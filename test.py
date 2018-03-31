import utils
import network as nw

def test_md5():
    assert utils.to_md5('{"lang":"en","uid":"999","accesstoken":"test"}') == '82842377366f62051e7e784aaff390f4'

def test_base64():
    assert utils.to_base64('{"lang":"en","uid":"999","accesstoken":"test"}') == 'eyJsYW5nIjoiZW4iLCJ1aWQiOiI5OTkiLCJhY2Nlc3N0b2tlbiI6InRlc3QifQ'

def test_generate_url():
    assert nw.Network.generate_url(php='test.php', lang='en', uid='999', accesstoken='test') == 'https://api.vhack.cc/mobile/14/test.php?user=eyJsYW5nIjoiZW4iLCJ1aWQiOiI5OTkiLCJhY2Nlc3N0b2tlbiI6InRlc3QifQ&pass=897823e153245f0ce9365268b0822072'
