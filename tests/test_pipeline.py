import copy,json,pathlib,sys,tempfile,unittest
from unittest.mock import patch
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'scripts'))
import collect,build
RULES=collect.read(collect.ROOT/'config/rules.json',{})
RSS=b'''<rss version="2.0"><channel><title>Test</title><item><title>\xe6\xab\xbb\xe5\x9d\x8246 MV</title><link>https://note.com/test/n/abc?utm_source=x</link><pubDate>Thu, 01 Jan 2026 09:00:00 +0900</pubDate><description>Test body</description></item></channel></rss>'''
class Rules(unittest.TestCase):
 def test_rss_dates(self):self.assertEqual(list(collect.parse(RSS))[0]['published_at'],'2026-01-01T00:00:00+00:00')
 def test_atom_original_not_updated(self):
  x=b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>A</title><link href="https://example.org/a"/><published>2020-01-01T00:00:00Z</published><updated>2026-01-01T00:00:00Z</updated></entry></feed>'
  self.assertTrue(list(collect.parse(x))[0]['published_at'].startswith('2020'))
 def test_no_fake_date(self):self.assertIsNone(collect.date('unknown'))
 def test_title_without_group(self):self.assertEqual(collect.classify('藤吉夏鈴はなぜ目を引くか','',RULES)[0],'published')
 def test_body_related(self):self.assertEqual(collect.classify('あの夜に見たもの','櫻坂46のライブを見た感想です',RULES)[0],'published')
 def test_unrelated(self):self.assertEqual(collect.classify('今日のお昼ご飯','カレーを食べた。',RULES)[0],'excluded')
 def test_ambiguous(self):self.assertEqual(collect.classify('最近の暮らし','櫻坂のCDも買いました。',RULES)[0],'pending')
 def test_cross_group_hold(self):self.assertEqual(collect.classify('乃木坂46 ライブ感想','櫻坂にも触れる',RULES)[0],'pending')
 def test_english_song_false_match(self):self.assertFalse(collect.song_match('BAN',collect.norm('urban research')))
 def test_promotion_hold(self):self.assertEqual(collect.classify('櫻坂46 自己紹介','',RULES)[0],'pending')
 def test_canonical(self):self.assertEqual(collect.canonical('https://note.com/test/n/abc?utm_source=x#foo'),'https://note.com/test/n/abc')
 def test_unsafe_link(self):
  with self.assertRaises(ValueError):collect.canonical('javascript:alert(1)')
 def test_entity_block(self):
  with self.assertRaises(ValueError):list(collect.parse(b'<!DOCTYPE rss [<!ENTITY x SYSTEM "file:///etc/passwd">]><rss/>'))
 def test_html_not_feed(self):
  with self.assertRaises(ValueError):list(collect.parse(b'<html/>'))

class Integration(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=pathlib.Path(self.tmp.name);self.mock=patch.object(collect,'ROOT',self.root);self.mock.start()
  collect.write(self.root/'config/rules.json',RULES)
  collect.write(self.root/'config/sources.json',[{'id':'test','url':'https://note.com/test','feed':'https://note.com/test/rss','enabled':True}])
  collect.write(self.root/'config/overrides.json',{})
  self.cache=self.root/'cache';self.cache.mkdir();(self.cache/'test.xml').write_bytes(RSS)
 def tearDown(self):self.mock.stop();self.tmp.cleanup()
 def rows(self):return collect.read(self.root/'state/articles.json',[])
 def test_dedup_and_date(self):
  collect.run(self.cache);collect.run(self.cache);self.assertEqual(len(self.rows()),1);self.assertEqual(self.rows()[0]['published_at'],'2026-01-01T00:00:00+00:00')
  self.assertNotIn('text',self.rows()[0])
 def test_failure_retains(self):
  collect.run(self.cache);(self.cache/'test.xml').write_bytes(b'broken');self.assertEqual(collect.run(self.cache),2);self.assertEqual(len(self.rows()),1)
 def test_takedown_not_reimported(self):
  collect.run(self.cache);collect.write(self.root/'config/overrides.json',{'blocked_urls':['https://note.com/test/n/abc']});collect.run(self.cache);self.assertEqual(self.rows(),[])
 def test_author_removed(self):
  collect.run(self.cache);collect.write(self.root/'config/overrides.json',{'blocked_authors':['test']});collect.run(self.cache);self.assertEqual(self.rows(),[])
 def test_future_hold(self):
  (self.cache/'test.xml').write_bytes(RSS.replace(b'2026',b'2099'));collect.run(self.cache);self.assertEqual(self.rows()[0]['status'],'pending')
 def test_absent_from_feed_retained(self):
  collect.run(self.cache);(self.cache/'test.xml').write_bytes(RSS.replace(b'/abc?',b'/def?'));collect.run(self.cache);self.assertEqual(len(self.rows()),2)
 def test_foreign_author_skipped(self):
  (self.cache/'test.xml').write_bytes(RSS.replace(b'/test/n/',b'/other/n/'));collect.run(self.cache);self.assertEqual(self.rows(),[])
if __name__=='__main__':unittest.main()
