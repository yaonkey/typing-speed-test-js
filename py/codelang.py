from github import Github
from sys import argv
import requests
import re
from random import choice


def get_contents_file(url: str, repo, src: str):
    contents = repo.get_contents(src)
    while len(contents) > 0:
        file_content = contents.pop(0)
        if file_content.type == 'dir':
            contents.extend(repo.get_contents(file_content.path))
        else:
            return file_content

def print_repo(repo, lang):
    # полное наименование репозитория
    print("Full name:", repo.full_name)
    # контент репозитория
    print("URL: ", repo.url)
    print("Contents:")
    for content in repo.get_contents(""):
        print(content.path)

class CodeLang:
    urls: list[str] = ['https://raw.githubusercontent.com/', '/master/']
    git = Github()
    av_langs: list = [
        'php', 'c', 'cpp', 'python',
        'javascript', 'html', 'css']
    filenames = [
        'main', 'index', 'config'
    ]
    is_avaliable: bool = False

    def __init__(self, lang: str):
        if lang in self.av_langs:
            self.lang = lang
            self.is_avaliable = True
        else:
            raise ValueError(f'Язык программирования {lang} недоступен!')

    def load_lang(self):
        '''Метод, позволяющий загрузить код по выбранному языку'''
        repos = self.git.search_repositories(query=f'language:{self.lang}')
        for repo in repos:
            # print_repo(repo, self.lang)  # use it for debug
            start_url = self.urls[0] + repo.full_name + '/master/'
            for name in self.filenames:
                if self.lang == 'javascript': 
                    self.url = start_url + f'{name}.js'
                elif self.lang == 'python':
                    self.url = start_url + f'{name}.py'
                else:
                    self.url = start_url + f'{name}.{self.lang}'
                page = requests.get(self.url)
                if page.status_code == 200:
                    return page.content.decode('utf-8')
                else:
                    continue

    def run(self):
        _langs = self.__getCode(self.lang)
        return choice(_langs)

    def __getCode(self, lang: str):
        '''Метод, возвращающий статичный код'''
        code_php = [
            '''<?php
function is_get() {
return $_SERVER['REQUEST_METHOD'] == 'GET';
}
function action() {
return isset($_GET['a']) ? $_GET['a'] : 'index';
}
function index() {
require 'manong.php';
exit;
}
function get_db() {
static $db = null;
if (is_null($db)) {
$db = new manongdb();
}
return $db;
}
$log = true;
function mylog($str) {
global $log;
if ($log) {
if (is_array($str)) {
echo "<pre>";
print_r($str);
echo "</pre>";
} else {
echo $str . '<br>';
}
}
}
function ajax_return($arr) {
header('Content-type:application/json;charset=utf-8');
echo json_encode($arr);
exit;
}
function crawl() {
$number = $_POST['number'];
$mdb = get_db();
$data = $mdb->get_issue($number);
$html = '';
if (empty($data)) {
$html .= 'no data';
} else {
$cates = $mdb->get_cate();
foreach ($data as $val) {
$cate = '';
foreach ($cates as $v) {
if (strlen($v) < 2) {
continue;
}
if (false !== strpos(strtoupper($val['title']), $v)) {
$cate = $v;
}
}
$html .= '<div class="item">';
$html .= '<hr>';
$html .= '<form>';
$html .= "<input type='hidden' name='id' value='{$val['id']}'>";
$html .= "<input type='hidden' name='number' value='{$val['number']}'>";
$html .= "<input type='text' class='newcate' name='newcate' value='{$cate}'>";
$html .= "</form>";
$html .= "</div>";
}
}
echo $html;
}
function cate() {
$mdb = get_db();
$cate = $mdb->get_cate();
$html = '';
$html .= '<select name="category">';
$catearr = [];
foreach ($cate as $val) {
$html .= '<option value="' . $val . '">' . $val . '</option>';
$catearr[] = $val;
}
$html .= '</select>';
ajax_return(['html' => $html, 'cate' => $catearr]);
}
function add() {
$cate = trim($_GET['newcate']);
$cate = $cate ? $cate : $_GET['category'];
$cate || ajax_return(['res' => 0, 'msg' => 'fill category']);
$data = [
'title' => trim($_GET['title']),
'desc' => trim($_GET['desc']),
'href' => trim($_GET['href']),
'number' => trim($_GET['number']),
'category' => mb_strtoupper($cate, 'utf-8'),
'hash' => md5(trim($_GET['href'])),
'addtime' => time(),
'ctime' => time(),
];
if (get_db()->add($data)) {
ajax_return(['res' => 1, 'msg' => 'success', 'cate' => $data['category']]);
} else {
ajax_return(['res' => 0, 'msg' => 'db error']);
}
}
function del() {
$id = $_GET['id'];
$rs = get_db()->del_cache($id);
$res = $rs ? 1 : 0;
ajax_return(compact('res'));
}
function render() {
$mdb = get_db();
$data = $mdb->get_all();
$current = $mdb->current_number();
$allContent = "";
$categories = $mdb->get_cate();
if ($categories) {
foreach ($categories as $val) {
$indexContent .= "[{$val}](#{$val})\n";
$filename = str_replace(['.', ' ', '/'], ['', '_', '_'], $val);
$readmeContent .= "[{$val}](category/{$filename}.md)  \n";
}
}
foreach ($data as $val) {
if ($val['category'] != $current_cate) {
$allContent .= "\n";
$allContent .= "<a name=\"{$val['category']}\"></a>\n";
$allContent .= "##" . str_replace('#', '\# ', $val['category']) . "\n";
$current_cate = $val['category'];
if (!empty($file_content)) {
file_put_contents($current_file, $file_content);
$file_content = '';
}
$current_file = 'category/' . str_replace(['.', ' ', '/'], ['', '_', '_'], $val['category']) . '.md';
}
$allContent .= "[{$val['title']}]({$val['href']})  \n";
$file_content .= "[{$val['title']}]({$val['href']})  \n";
}
$rs = file_put_contents('./readme.md', $readmeContent);
file_put_contents('./category/all.md', $indexContent . $allContent);
if ($rs) {
ajax_return(['res' => 1]);
} else {
}
}
class manongdb {
private $pdo;
function __construct($user = 'root', $password = '', $dbname = 'manong') {
$this->pdo = new PDO('mysql:host=localhost;dbname=' . $dbname, $user, $password);
$this->pdo->query('set names utf8');
}
function get_issue($number) {
mylog('searching for cache');
$data = $this->cache($number);
if (empty($data)) {
mylog('no cache,start crawling');
$data = $this->crawl($number);
if (false === $data) {
}
}
return $data;
}
function cache($number) {
$data = $this->pdo->query("select * from cache where number={$number}")->fetchAll(PDO::FETCH_ASSOC);
if ($data) {
mylog('cache founded');
}
return $data;
}
function del_cache($id) {
return $this->pdo->exec("delete from cache where id={$id}");
}
function crawl($number) {
$url = $this->issue_url . $number;
$content = file_get_contents($url);
$content = str_replace(["\r", "\n"], '', $content);
if ($number >= 91) {
$pattern = '/<h4><a target="_blank" href="(.*?)">(.*?)<\/a>&nbsp;&nbsp;
(?:<a target="_blank".*?<\/a>)?<\/h4>.*?<p>(.*?)<\/p>/';
} else {
$pattern = '/<h4><a target="_blank" href="(.*?)">(.*?)<\/a>&nbsp;&nbsp;
<\/h4>.*?<p>(.*?)<\/p>/';
}
$rs = preg_match_all($pattern, $content, $matches);
if ($rs) {
mylog('crawl finished.start parsing');
$data = array();
foreach ($matches[1] as $key => $val) {
if (false !== strpos($matches[1][$key], 'job') || false !== strpos($matches[1][$key], 'amazon')) {
continue;
}
$item = [
'title' => strip_tags($matches[2][$key]),
'desc' => $matches[3][$key],
'href' => $val,
'number' => $number,
'hash' => md5($val),
];
$id = $this->add_cache($item);
$item['id'] = $id;
mylog("item {$id} added to cache");
$data[] = $item;
}
return $data;
}
mylog('failed to crawl');
return false;
}
function add_cache($item) {
$sql = $this->arr2sql('cache', $item);
$this->pdo->exec($sql);
$id = $this->pdo->lastInsertId();
return $id;
}
function arr2sql($dbname, $arr, $updateid = null) {
if ($updateid) {
unset($arr['ctime']);
unset($arr['addtime']);
$sql = "update {$dbname} set ";
foreach ($arr as $key => $val) {
$sql .= "`{$key}`='{$val}',";
}
$sql .= 'ctime=' . time();
$sql .= " where id={$updateid}";
return $sql;
} else {
$fields = [];
$values = [];
foreach ($arr as $key => $v) {
$fields[] = "`{$key}`";
$values[] = "'{$v}'";
}
return "insert into {$dbname} (" . implode(',', $fields) . ") values(" . implode(',', $values) . ")";
}
}
function get_cate() {
$arr = [];
$rs = $this->pdo->query("select distinct category from issue order by category")->fetchAll(PDO::FETCH_ASSOC);
foreach ($rs as $val) {
$arr[] = $val['category'];
}
return $arr;
}
function add($data) {
$sql = $this->arr2sql('issue', $data);
$rs = $this->pdo->exec($sql);
if ($rs) {
return $this->pdo->lastInsertId();
}
$rs = $this->pdo->query("select id from issue where hash='{$data['hash']}'")->fetch(PDO::FETCH_ASSOC);
if (isset($rs['id'])) {
$update = $this->pdo->exec($this->arr2sql('issue', $data, $rs['id']));
if ($update) {
return $rs['id'];
}
}
return false;
}
function get_all() {
return $this->pdo->query('select * from issue order by category,addtime')->fetchAll(PDO::FETCH_ASSOC);
}
function current_number() {
$rs = $this->pdo->query('select max(number) as max from issue')->fetch(PDO::FETCH_ASSOC);
return $rs['max'];
}
}
?>''',
'''<?php
namespace Symfony\Component\BrowserKit\Tests;
use PHPUnit\Framework\TestCase;
use Symfony\Component\BrowserKit\CookieJar;
use Symfony\Component\BrowserKit\Exception\BadMethodCallException;
use Symfony\Component\BrowserKit\History;
use Symfony\Component\BrowserKit\Request;
use Symfony\Component\BrowserKit\Response;
class AbstractBrowserTest extends TestCase
{
{
return new TestClient($server, $history, $cookieJar);
}
public function testGetHistory()
{
$client = $this->getBrowser([], $history = new History());
$this->assertSame($history, $client->getHistory(), '->getHistory() returns the History');
}
public function testGetCookieJar()
{
$client = $this->getBrowser([], null, $cookieJar = new CookieJar());
}
public function testGetRequest()
{
$client = $this->getBrowser();
$client->request('GET', 'http://example.com/');
}
public function testGetRequestNull()
{
$this->expectException(BadMethodCallException::class);
$client = $this->getBrowser();
$this->assertNull($client->getRequest());
}
public function testXmlHttpRequest()
{
$client = $this->getBrowser();
$client->xmlHttpRequest('GET', 'http://example.com/', [], [], [], null, true);
$this->assertSame('XMLHttpRequest', $client->getRequest()->getServer()['HTTP_X_REQUESTED_WITH']);
$this->assertFalse($client->getServerParameter('HTTP_X_REQUESTED_WITH', false));
}
public function testJsonRequest()
{
$client = $this->getBrowser();
$client->jsonRequest('GET', 'http://example.com/', ['param' => 1], [], true);
$this->assertSame('application/json', $client->getRequest()->getServer()['CONTENT_TYPE']);
$this->assertSame('application/json', $client->getRequest()->getServer()['HTTP_ACCEPT']);
$this->assertFalse($client->getServerParameter('CONTENT_TYPE', false));
$this->assertFalse($client->getServerParameter('HTTP_ACCEPT', false));
$this->assertSame('{"param":1}', $client->getRequest()->getContent());
}
public function testGetRequestWithIpAsHttpHost()
{
$client = $this->getBrowser();
$client->request('GET', 'https://example.com/foo', [], [], ['HTTP_HOST' => '127.0.0.1']);
$this->assertSame('https://example.com/foo', $client->getRequest()->getUri());
$headers = $client->getRequest()->getServer();
$this->assertSame('127.0.0.1', $headers['HTTP_HOST']);
}
public function testGetResponse()
{
$client = $this->getBrowser();
$client->setNextResponse(new Response('foo'));
$client->request('GET', 'http://example.com/');
}
public function testGetResponseNull()
{
$this->expectException(BadMethodCallException::class);
$client = $this->getBrowser();
$this->assertNull($client->getResponse());
}
public function testGetInternalResponseNull()
{
$this->expectException(BadMethodCallException::class);
$client = $this->getBrowser();
$this->assertNull($client->getInternalResponse());
}
public function testGetContent()
{
$json = '{"jsonrpc":"2.0","method":"echo","id":7,"params":["Hello World"]}';
$client = $this->getBrowser();
$client->request('POST', 'http://example.com/jsonrpc', [], [], [], $json);
$this->assertSame($json, $client->getRequest()->getContent());
}
public function testGetCrawler()
{
$client = $this->getBrowser();
$client->setNextResponse(new Response('foo'));
$crawler = $client->request('GET', 'http://example.com/');
}
public function testGetCrawlerNull()
{
$this->expectException(BadMethodCallException::class);
$client = $this->getBrowser();
$this->assertNull($client->getCrawler());
}
public function testRequestHttpHeaders()
{
$client = $this->getBrowser();
$client->request('GET', '/');
$headers = $client->getRequest()->getServer();
$this->assertSame('localhost', $headers['HTTP_HOST'], '->request() sets the HTTP_HOST header');
$client = $this->getBrowser();
$client->request('GET', 'http://www.example.com');
$headers = $client->getRequest()->getServer();
$this->assertSame('www.example.com', $headers['HTTP_HOST'], '->request() sets the HTTP_HOST header');
$client->request('GET', 'https://www.example.com');
$headers = $client->getRequest()->getServer();
$this->assertTrue($headers['HTTPS'], '->request() sets the HTTPS header');
$client = $this->getBrowser();
$client->request('GET', 'http://www.example.com:8080');
$headers = $client->getRequest()->getServer();
public function testRequestURIConversion()
{
$client = $this->getBrowser();
$client->request('GET', '/foo');
$client = $this->getBrowser();
$client->request('GET', 'http://www.example.com');
$client = $this->getBrowser();
$client->request('GET', 'http://www.example.com/');
$client->request('GET', '/foo');
$client = $this->getBrowser();
$client->request('GET', 'http://www.example.com/foo');
$client->request('GET', '#');
public function testRequestRefererCanBeOverridden()
{
$client = new TestClient();
$client->request('GET', 'http://www.example.com/foo/foobar');
$client->request('GET', 'bar', [], [], ['HTTP_REFERER' => 'xyz']);
$server = $client->getRequest()->getServer();
$this->assertSame('xyz', $server['HTTP_REFERER'], '->request() allows referer to be overridden');
public function testRequestHistory()
{
$client = $this->getBrowser();
$client->request('GET', 'http://www.example.com/foo/foobar');
$client->request('GET', 'bar');
}
public function testRequestCookies()
{
$client = $this->getBrowser();
$client->setNextResponse(new Response('<html><a href="/foo">foo</a></html>', 200, ['Set-Cookie' => 'foo=bar']));
$client->request('GET', 'http://www.example.com/foo/foobar');
$client->request('GET', 'bar');
}

public function testRequestSecureCookies()
{
$client = $this->getBrowser();
$client->request('GET', 'https://www.example.com/foo/foobar');
$this->assertTrue($client->getCookieJar()->get('foo', '/', 'www.example.com')->isSecure());
}
public function testClick()
{
$client = $this->getBrowser();
$client->setNextResponse(new Response('<html><a href="/foo">foo</a></html>'));
$crawler = $client->request('GET', 'http://www.example.com/foo/foobar');
$client->click($crawler->filter('a')->link());
$this->assertSame('http://www.example.com/foo', $client->getRequest()->getUri(), '->click() clicks on links');
}
public function testClickLink()
{
$client = $this->getBrowser();
$client->setNextResponse(new Response('<html><a href="/foo">foo</a></html>'));
$client->request('GET', 'http://www.example.com/foo/foobar');
$client->clickLink('foo');
$this->assertSame('http://www.example.com/foo', $client->getRequest()->getUri(), '->click() clicks on links');
}
public function testClickLinkNotFound()
{
$client = $this->getBrowser();
$client->setNextResponse(new Response('<html><a href="/foo">foobar</a></html>'));
$client->request('GET', 'http://www.example.com/foo/foobar');
try {
$client->clickLink('foo');
$this->fail('->clickLink() throws a \InvalidArgumentException if the link could not be found');
} catch (\Exception $e) {
}
}
public function testClickForm()
{
$client = $this->getBrowser();
$client->setNextResponse(new Response('<html><form action="/foo"><input type="submit" /></form></html>'));
$crawler = $client->request('GET', 'http://www.example.com/foo/foobar');
$client->click($crawler->filter('input')->form());
}
public function testSubmit()
{
$client = $this->getBrowser();
$crawler = $client->request('GET', 'http://www.example.com/foo/foobar');
$client->submit($crawler->filter('input')->form());
$this->assertSame('http://www.example.com/foo', $client->getRequest()->getUri(), '->submit() submit forms');
}
public function testSubmitForm()
{
$client = $this->getBrowser();
$client->request('GET', 'http://www.example.com/foo/foobar');
$client->submitForm('Register', [
'username' => 'new username',
'password' => 'new password',
], 'PUT', [
'HTTP_USER_AGENT' => 'Symfony User Agent',
]);
$this->assertSame('http://www.example.com/foo', $client->getRequest()->getUri(), '->submitForm() submit forms');
$this->assertSame('PUT', $client->getRequest()->getMethod(), '->submitForm() allows to change the method');
}
public function testSubmitFormNotFound()
{
$client = $this->getBrowser();
$client->setNextResponse(new Response('<html><form action="/foo"><input type="submit" /></form></html>'));
$client->request('GET', 'http://www.example.com/foo/foobar');
try {
$client->submitForm('Register', [
'username' => 'username',
'password' => 'password',
], 'POST');
$this->fail('->submitForm() throws a \InvalidArgumentException if the form could not be found');
} catch (\Exception $e) {
}
}
public function testSubmitPreserveAuth()
{
$client = $this->getBrowser(['PHP_AUTH_USER' => 'foo', 'PHP_AUTH_PW' => 'bar']);
$client->setNextResponse(new Response('<html><form action="/foo"><input type="submit" /></form></html>'));
$crawler = $client->request('GET', 'http://www.example.com/foo/foobar');
$server = $client->getRequest()->getServer();
$this->assertArrayHasKey('PHP_AUTH_USER', $server);
$this->assertSame('foo', $server['PHP_AUTH_USER']);
$this->assertArrayHasKey('PHP_AUTH_PW', $server);
$this->assertSame('bar', $server['PHP_AUTH_PW']);
$client->submit($crawler->filter('input')->form());
$this->assertSame('http://www.example.com/foo', $client->getRequest()->getUri(), '->submit() submit forms');
$server = $client->getRequest()->getServer();
$this->assertArrayHasKey('PHP_AUTH_USER', $server);
$this->assertSame('foo', $server['PHP_AUTH_USER']);
$this->assertArrayHasKey('PHP_AUTH_PW', $server);
$this->assertSame('bar', $server['PHP_AUTH_PW']);
}
public function testSubmitPassthrewHeaders()
{
$client = $this->getBrowser();
$client->setNextResponse(new Response('<html><form action="/foo"><input type="submit" /></form></html>'));
$crawler = $client->request('GET', 'http://www.example.com/foo/foobar');
$headers = ['Accept-Language' => 'de'];
$client->submit($crawler->filter('input')->form(), [], $headers);
$server = $client->getRequest()->getServer();
$this->assertArrayHasKey('Accept-Language', $server);
$this->assertSame('de', $server['Accept-Language']);
}
public function testFollowRedirect()
{
$client = $this->getBrowser();
$client->followRedirects(false);
$client->request('GET', 'http://www.example.com/foo/foobar');
try {
$client->followRedirect();
$this->fail('->followRedirect() throws a \LogicException if the request was not redirected');
} catch (\Exception $e) {
}
$client->setNextResponse(new Response('', 302, ['Location' => 'http://www.example.com/redirected']));
$client->request('GET', 'http://www.example.com/foo/foobar');
$client->followRedirect();
$client = $this->getBrowser();
$client->setNextResponse(new Response('', 302, ['Location' => 'http://www.example.com/redirected']));
$client->request('GET', 'http://www.example.com/foo/foobar');
$client = $this->getBrowser();
$client->setNextResponse(new Response('', 201, ['Location' => 'http://www.example.com/redirected']));
$client->request('GET', 'http://www.example.com/foo/foobar');
$client = $this->getBrowser();
$client->setNextResponse(new Response('', 201, ['Location' => 'http://www.example.com/redirected']));
$client->followRedirects(false);
$client->request('GET', 'http://www.example.com/foo/foobar');
try {
$client->followRedirect();
$this->fail('->followRedirect() throws a \LogicException if the request did not respond with 30x HTTP Code');
} catch (\Exception $e) {
}
}
public function testFollowRelativeRedirect()
{
$client = $this->getBrowser();
$client->setNextResponse(new Response('', 302, ['Location' => '/redirected']));
$client->request('GET', 'http://www.example.com/foo/foobar');
$client = $this->getBrowser();
$client->setNextResponse(new Response('', 302, ['Location' => '/redirected:1234']));
$client->request('GET', 'http://www.example.com/foo/foobar');
}
public function testFollowRedirectWithMaxRedirects()
{
$client = $this->getBrowser();
$client->setMaxRedirects(1);
$client->setNextResponse(new Response('', 302, ['Location' => 'http://www.example.com/redirected']));
$client->request('GET', 'http://www.example.com/foo/foobar');
$client->setNextResponse(new Response('', 302, ['Location' => 'http://www.example.com/redirected2']));
try {
$client->followRedirect();
$this->fail('->followRedirect() throws a \LogicException if the request was redirected and limit of redirections was reached');
} catch (\Exception $e) {
}
$client->setNextResponse(new Response('', 302, ['Location' => 'http://www.example.com/redirected']));
$client->request('GET', 'http://www.example.com/foo/foobar');
$client->setNextResponse(new Response('', 302, ['Location' => '/redirected']));
$client->request('GET', 'http://www.example.com/foo/foobar');
$client = $this->getBrowser();
$client->setNextResponse(new Response('', 302, ['Location' => '//www.example.org/']));
$client->request('GET', 'https://www.example.com/');
''',
'''public static function get_last_query($connection_name = null) {
if ($connection_name === null) {
return self::$_last_query;
}
if (!isset(self::$_query_log[$connection_name])) {
return '';
}
return end(self::$_query_log[$connection_name]);
}
public static function get_query_log($connection_name = self::DEFAULT_CONNECTION) {
if (isset(self::$_query_log[$connection_name])) {
return self::$_query_log[$connection_name];
}
return array();
}
public static function get_connection_names() {
return array_keys(self::$_db);
}
protected function __construct($table_name, $data = array(), $connection_name = self::DEFAULT_CONNECTION) {
$this->_table_name = $table_name;
$this->_data = $data;

$this->_connection_name = $connection_name;
self::_setup_db_config($connection_name);
}
public function create($data=null) {
$this->_is_new = true;
if (!is_null($data)) {
return $this->hydrate($data)->force_all_dirty();
}
return $this;
}
public function use_id_column($id_column) {
$this->_instance_id_column = $id_column;
return $this;
}
protected function _create_instance_from_row($row) {
$instance = self::for_table($this->_table_name, $this->_connection_name);
$instance->use_id_column($this->_instance_id_column);
$instance->hydrate($row);
return $instance;
}
public function find_one($id=null) {
if (!is_null($id)) {
$this->where_id_is($id);
}
$this->limit(1);
$rows = $this->_run();

if (empty($rows)) {
return false;
}

return $this->_create_instance_from_row($rows[0]);
}
public function find_many() {
if(self::$_config[$this->_connection_name]['return_result_sets']) {
return $this->find_result_set();
}
return $this->_find_many();
}
protected function _find_many() {
$rows = $this->_run();
return array_map(array($this, '_create_instance_from_row'), $rows);
}
public function find_result_set() {
return new IdiormResultSet($this->_find_many());
}
public function find_array() {
return $this->_run(); 
}
public function count($column = '*') {
return $this->_call_aggregate_db_function(__FUNCTION__, $column);
}
public function max($column)  {
return $this->_call_aggregate_db_function(__FUNCTION__, $column);
}
public function min($column)  {
return $this->_call_aggregate_db_function(__FUNCTION__, $column);
}
public function avg($column)  {
return $this->_call_aggregate_db_function(__FUNCTION__, $column);
}
public function sum($column)  {
return $this->_call_aggregate_db_function(__FUNCTION__, $column);
}
protected function _call_aggregate_db_function($sql_function, $column) {
$alias = strtolower($sql_function);
$sql_function = strtoupper($sql_function);
if('*' != $column) {
$column = $this->_quote_identifier($column);
}
$result_columns = $this->_result_columns;
$this->_result_columns = array();
$this->select_expr("$sql_function($column)", $alias);
$result = $this->find_one();
$this->_result_columns = $result_columns;
$return_value = 0;
if($result !== false && isset($result->$alias)) {
if (!is_numeric($result->$alias)) {
$return_value = $result->$alias;
}
elseif((int) $result->$alias == (float) $result->$alias) {
$return_value = (int) $result->$alias;
} else {
$return_value = (float) $result->$alias;
}
}
return $return_value;
}
public function hydrate($data=array()) {
$this->_data = $data;
return $this;
}
public function force_all_dirty() {
$this->_dirty_fields = $this->_data;
return $this;
}
public function raw_query($query, $parameters = array()) {
$this->_is_raw_query = true;
$this->_raw_query = $query;
$this->_raw_parameters = $parameters;
return $this;
}
public function table_alias($alias) {
$this->_table_alias = $alias;
return $this;
}''']  # code_php
        code_c = [
'''
#include <syscall/mm.h>
#include <heap.h>
#include <log.h>
struct bucket
{
int ref_cnt;
void *first_free;
struct bucket *next_bucket;
};
struct pool
{
int objsize;
struct bucket *first;
};
#define POOL_COUNT	11
struct heap_data
{
SRWLOCK rw_lock;
struct pool pools[POOL_COUNT];
};
static struct heap_data *heap;
void heap_init()
{
log_info("heap subsystem initializating...");
heap = mm_static_alloc(sizeof(struct heap_data));
InitializeSRWLock(&heap->rw_lock);
heap->pools[0].objsize = 16;		
heap->pools[0].first = NULL;
heap->pools[1].objsize = 32;		
heap->pools[1].first = NULL;
heap->pools[2].objsize = 64;		
heap->pools[2].first = NULL;
heap->pools[3].objsize = 128;		
heap->pools[3].first = NULL;
heap->pools[4].objsize = 256;		
heap->pools[4].first = NULL;
heap->pools[5].objsize = 512;		
heap->pools[5].first = NULL;
heap->pools[6].objsize = 1024;		
heap->pools[6].first = NULL;
heap->pools[7].objsize = 2048;		
heap->pools[7].first = NULL;
heap->pools[8].objsize = 4096;		
heap->pools[8].first = NULL;
heap->pools[9].objsize = 8192;		
heap->pools[9].first = NULL;
heap->pools[10].objsize = 16384;	
heap->pools[10].first = NULL;
log_info("heap subsystem initialized.");
}
int heap_fork(HANDLE process)
{
AcquireSRWLockShared(&heap->rw_lock);
return 1;
}
void heap_afterfork_parent()
{
ReleaseSRWLockShared(&heap->rw_lock);
}
void heap_afterfork_child()
{
heap = mm_static_alloc(sizeof(struct heap_data));
InitializeSRWLock(&heap->rw_lock);
}
#define ALIGN(x, align) (((x) + ((align) - 1)) & -(align))
static struct bucket *alloc_bucket(int objsize)
{
struct bucket *b = mm_mmap(NULL, BLOCK_SIZE, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE,
INTERNAL_MAP_TOPDOWN | INTERNAL_MAP_NORESET | INTERNAL_MAP_VIRTUALALLOC, NULL, 0);
b->ref_cnt = 0;
b->next_bucket = NULL;
char *c = (char *)b + ALIGN(sizeof(struct bucket), sizeof(void *));
b->first_free = c;
while (c + objsize < (char *)b + BLOCK_SIZE)
{
*(char **)c = c + objsize;
c += objsize;
}
*(char **)c = NULL;
return b;
}
void *kmalloc(int size)
{
AcquireSRWLockExclusive(&heap->rw_lock);
int p = -1;
for (int i = 0; i < POOL_COUNT; i++)
if (size <= heap->pools[i].objsize)
{
p = i;
break;
}
if (p == -1)
{
log_error("kmalloc(%d): size too large.", size);
ReleaseSRWLockExclusive(&heap->rw_lock);
return NULL;
}
if (!heap->pools[p].first)
heap->pools[p].first = alloc_bucket(heap->pools[p].objsize);
struct bucket *current = heap->pools[p].first;
for (;;)
{
if (!current)
{
log_error("kmalloc(%d): out of memory", size);
ReleaseSRWLockExclusive(&heap->rw_lock);
return NULL;
}
if (current->first_free)
{
void *c = current->first_free;
current->first_free = *(void**)c;
current->ref_cnt++;
ReleaseSRWLockExclusive(&heap->rw_lock);
return c;
}
if (!current->next_bucket)
current->next_bucket = alloc_bucket(heap->pools[p].objsize);
current = current->next_bucket;
}
}
void kfree(void *mem, int size)
{
AcquireSRWLockExclusive(&heap->rw_lock);
void *bucket_addr = (void *)((size_t) mem & (-BLOCK_SIZE));
int p = -1;
for (int i = 0; i < POOL_COUNT; i++)
if (size <= heap->pools[i].objsize)
{
p = i;
break;
}
if (p == -1)
{
log_error("kfree(): Invalid size: %x", mem);
ReleaseSRWLockExclusive(&heap->rw_lock);
return;
}
struct bucket *previous = NULL;
struct bucket *current = heap->pools[p].first;
while (current)
{
if (current != bucket_addr)
{
previous = current;
current = current->next_bucket;
continue;
}
*(void **)mem = current->first_free;
current->first_free = mem;
current->ref_cnt--;
if (!current->ref_cnt)
{
if (!previous)
heap->pools[p].first = current->next_bucket;
else
previous->next_bucket = current->next_bucket;
mm_munmap(current, BLOCK_SIZE);
}
ReleaseSRWLockExclusive(&heap->rw_lock);
return;
}
log_error("kfree(): Invalid memory pointer or size: (%x, %d)", mem, size);
ReleaseSRWLockExclusive(&heap->rw_lock);
}''',
'''
#include <common/auxvec.h>
#include <common/errno.h>
#include <syscall/exec.h>
#include <syscall/fork.h>
#include <syscall/mm.h>
#include <syscall/process.h>
#include <syscall/sig.h>
#include <syscall/tls.h>
#include <syscall/vfs.h>
#include <flags.h>
#include <log.h>
#include <heap.h>
#include <shared.h>
#include <str.h>
#include <version.h>
#include <win7compat.h>
#define WIN32_LEAN_AND_MEAN
#include <Windows.h>
#pragma comment(linker,"/entry:main")
#pragma comment(lib,"delayimp")
#ifdef _DEBUG
#pragma comment(lib,"libucrtd")
#else
#pragma comment(lib,"libucrt")
#endif
char *startup;
static void init_subsystems()
{
shared_init();
heap_init();
signal_init();
process_init();
tls_init();
vfs_init();
dbt_init();
}
#define ENV(x) 
do { 
memcpy(envbuf, x, sizeof(x)); 
envbuf += sizeof(x); 
} while (0)
void main()
{
win7compat_init();
log_init();
fork_init();
mm_init();
flags_init();
const char *cmdline = GetCommandLineA();
int len = strlen(cmdline);
if (len > BLOCK_SIZE) /* TODO: Test if there is sufficient space for argv[] array */
{
init_subsystems();
kprintf("Command line too long.\n");
process_exit(1, 0);
}
startup = mm_mmap(NULL, BLOCK_SIZE, PROT_READ | PROT_WRITE, MAP_ANONYMOUS,
INTERNAL_MAP_TOPDOWN | INTERNAL_MAP_NORESET | INTERNAL_MAP_VIRTUALALLOC, NULL, 0);
*(uintptr_t*) startup = 1;
char *current_startup_base = startup + sizeof(uintptr_t);
memcpy(current_startup_base, cmdline, len + 1);
char *envbuf = (char *)ALIGN_TO(current_startup_base + len + 1, sizeof(void*));
char *env0 = envbuf;
ENV("TERM=xterm");
char *env1 = envbuf;
ENV("HOME=/root");
char *env2 = envbuf;
ENV("DISPLAY=127.0.0.1:0");
char *env3 = envbuf;
ENV("PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/bin:/sbin");
int argc = 0;
char **argv = (char **)ALIGN_TO(envbuf, sizeof(void*));
int in_quote = 0;
char *j = current_startup_base;
for (char *i = current_startup_base; i <= current_startup_base + len; i++)
if (!in_quote && (*i == ' ' || *i == '\t' || *i == '\r' || *i == '\n' || *i == 0))
{
*i = 0;
if (i > j)
argv[argc++] = j;
j = i + 1;
}
else if (*i == '"')
{
*i = 0;
if (in_quote)
argv[argc++] = j;
in_quote = !in_quote;
j = i + 1;
}
argv[argc] = NULL;
char **envp = argv + argc + 1;
int env_size = 4;
envp[0] = env0;
envp[1] = env1;
envp[2] = env2;
envp[3] = env3;
envp[4] = NULL;
char *buffer_base = (char*)(envp + env_size + 1);
const char *filename = NULL;
int arg_start;
for (int i = 1; i < argc; i++)
{
if (!strcmp(argv[i], "--session-id"))
{
if (++i < argc)
{
int len = strlen(argv[i]);
if (len >= MAX_SESSION_ID_LEN)
{
init_subsystems();
kprintf("--session-id: Session ID too long.\n");
process_exit(1, 0);
}
for (int j = 0; j < len; j++)
{
char ch = argv[i][j];
if (!((ch >= '0' && ch <= '9') || (ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z') ||
ch == '_' || ch == '-'))
{
init_subsystems();
kprintf("--session-id: Invalid characters.\n");
process_exit(1, 0);
}
}
strcpy(cmdline_flags->global_session_id, argv[i]);
}
else
{
init_subsystems();
kprintf("--session-id: No ID given.\n");
process_exit(1, 0);
}
}
else if (!strcmp(argv[i], "--help") || !strcmp(argv[i], "-h"))
{
init_subsystems();
print_help();
process_exit(1, 0);
}
else if (!strcmp(argv[i], "--usage"))
{
init_subsystems();
print_usage();
process_exit(1, 0);
}
else if (!strcmp(argv[i], "--version") || !strcmp(argv[i], "-v"))
{
init_subsystems();
print_version();
process_exit(1, 0);
}
else if (!strcmp(argv[i], "--dbt-trace"))
cmdline_flags->dbt_trace = true;
else if (!strcmp(argv[i], "--dbt-trace-all"))
{
cmdline_flags->dbt_trace = true;
cmdline_flags->dbt_trace_all = true;
}
else if (argv[i][0] == '-')
{
init_subsystems();
kprintf("Unrecognized option: %s\n", argv[i]);
process_exit(1, 0);
}
else if (!filename)
{
filename = argv[i];
arg_start = i;
break;
}
}
init_subsystems();
if (filename)
{
install_syscall_handler();
if (r == -L_ENOENT)
{
kprintf("Executable not found.");
process_exit(1, 0);
}
}
print_usage();
process_exit(1, 0);
}''',
'''
#include "phenom/sysutil.h"
#include "phenom/memory.h"
#include "phenom/stream.h"
#include "phenom/log.h"
#include <pthread.h>
static ph_memtype_t mt_stm;
static ph_memtype_def_t stm_def = {
"stream", "stream", 0, 0
};
static pthread_mutexattr_t mtx_attr;
void ph_stm_lock(ph_stream_t *stm)
{
int res = pthread_mutex_lock(&stm->lock);
if (ph_unlikely(res != 0)) {
ph_panic("ph_stm_lock: `Pe%d", res);
}
}
void ph_stm_unlock(ph_stream_t *stm)
{
int res = pthread_mutex_unlock(&stm->lock);
if (ph_unlikely(res != 0)) {
ph_panic("ph_stm_unlock: `Pe%d", res);
}
}
ph_stream_t *ph_stm_make(const struct ph_stream_funcs *funcs,
void *cookie, int flags, uint32_t bufsize)
{
ph_stream_t *stm;
int err;
stm = ph_mem_alloc_size(mt_stm, sizeof(*stm) + PH_STM_UNGET + bufsize);
if (!stm) {
return NULL;
}
memset(stm, 0, sizeof(*stm));
err = pthread_mutex_init(&stm->lock, &mtx_attr);
if (err) {
ph_mem_free(mt_stm, stm);
errno = err;
return NULL;
}
stm->buf = (unsigned char*)stm + sizeof(*stm) + PH_STM_UNGET;
stm->bufsize = bufsize;
stm->funcs = funcs;
stm->cookie = cookie;
stm->flags = flags;
return stm;
}
void ph_stm_destroy(ph_stream_t *stm)
{
if (stm->flags & PH_STM_FLAG_ONSTACK) {
ph_panic("ph_stm_destroy: this stream is not a heap instance!");
}
ph_mem_free(mt_stm, stm);
}
bool ph_stm_close(ph_stream_t *stm)
{
if (!ph_stm_flush(stm)) {
return false;
}
if (!stm->funcs->close(stm)) {
errno = ph_stm_errno(stm);
return false;
}
if ((stm->flags & PH_STM_FLAG_ONSTACK) == 0) {
ph_mem_free(mt_stm, stm);
}
return true;
}
static void stm_init(void)
{
int err;
mt_stm = ph_memtype_register(&stm_def);
if (mt_stm == PH_MEMTYPE_INVALID) {
ph_panic("stm_init: unable to register memory types");
}
err = pthread_mutexattr_init(&mtx_attr);
if (err) {
ph_panic("stm_init: mutexattr_init: `Pe%d", err);
}
err = pthread_mutexattr_settype(&mtx_attr, PTHREAD_MUTEX_ERRORCHECK);
if (err) {
ph_panic("stm_init: mutexattr ERRORCHECK: `Pe%d", err);
}
}
PH_LIBRARY_INIT_PRI(stm_init, 0, 7)
''']  # code_c
        code_cpp = [
            '''#include <windows.h>
#include <process.h>
#include <tchar.h>
#include <stdio.h>
#include "SystemInfo.h"
#include <sstream>
using std::stringstream;
#ifndef WINNT
#error You need Windows NT to use this source code. Define WINNT!
#endif
void SystemInfoUtils::LPCWSTR2string( LPCWSTR strW, string& str )
{
#ifdef UNICODE
str = strW;
#else
str = _T("");
TCHAR* actChar = (TCHAR*)strW;
if ( actChar == _T('\0') )
return;
ULONG len = wcslen(strW) + 1;
TCHAR* pBuffer = new TCHAR[ len ];
TCHAR* pNewStr = pBuffer;
while ( len-- )
{
*(pNewStr++) = *actChar;
actChar += 2;
}
str = pBuffer;
delete [] pBuffer;
#endif
}
void SystemInfoUtils::Unicode2string( UNICODE_STRING* strU, string& str )
{
if ( *(DWORD*)strU != 0 )
LPCWSTR2string( (LPCWSTR)strU->Buffer, str );
else
str = _T("");
}
BOOL SystemInfoUtils::GetFsFileName( LPCTSTR lpDeviceFileName,
string& fsFileName )
{
BOOL rc = FALSE;
TCHAR lpDeviceName[0x1000];
TCHAR lpDrive[3] = _T("A:");
for ( TCHAR actDrive = _T('A'); actDrive <= _T('Z'); actDrive++ ) {
lpDrive[0] = actDrive;
if ( QueryDosDevice( lpDrive, lpDeviceName, 0x1000 ) != 0 ) {
if ( _tcsnicmp( _T("\\Device\\LanmanRedirector\\"),
lpDeviceName, 25 ) == 0 ) {
char cDriveLetter;
DWORD dwParam;
TCHAR lpSharedName[0x1000];
```,
```
if ( _stscanf(  lpDeviceName, 
_T("\\Device\\LanmanRedirector\\;%c:%d\\%s"), 
&cDriveLetter, 
&dwParam, 
lpSharedName ) != 3 )
continue;
_tcscpy( lpDeviceName,
_T("\\Device\\LanmanRedirector\\") );
_tcscat( lpDeviceName, lpSharedName );
}
if ( _tcsnicmp( lpDeviceName, lpDeviceFileName,
_tcslen( lpDeviceName ) ) == 0 )
{
fsFileName = lpDrive;
fsFileName += (LPCTSTR)( lpDeviceFileName
+ _tcslen( lpDeviceName ) );
rc = TRUE;
break;
}
}
}
return rc;
}
BOOL SystemInfoUtils::GetDeviceFileName( LPCTSTR lpFsFileName,
string& deviceFileName )
{
BOOL rc = FALSE;
TCHAR lpDrive[3];
_tcsncpy( lpDrive, lpFsFileName, 2 );
lpDrive[2] = _T('\0');
TCHAR lpDeviceName[0x1000];
```,
```
if ( QueryDosDevice( lpDrive, lpDeviceName, 0x1000 ) != 0 )
{
if ( _tcsnicmp( _T("\\??\\"), lpDeviceName, 4 ) == 0 )
{
deviceFileName = lpDeviceName + 4;
deviceFileName += lpFsFileName + 2;
return TRUE;
}
else
if ( _tcsnicmp( _T("\\Device\\LanmanRedirector\\"),
lpDeviceName, 25 ) == 0 ) {
char cDriveLetter;
DWORD dwParam;
TCHAR lpSharedName[0x1000];
if ( _stscanf(  lpDeviceName, 
_T("\\Device\\LanmanRedirector\\;%c:%d\\%s"), 
&cDriveLetter, 
&dwParam, 
lpSharedName ) != 3 )
return FALSE;
_tcscpy( lpDeviceName,
_T("\\Device\\LanmanRedirector\\") );
_tcscat( lpDeviceName, lpSharedName );
}
_tcscat( lpDeviceName, lpFsFileName + 2 );
```, ```
deviceFileName = lpDeviceName;
rc = TRUE;
}
return rc;
}
DWORD SystemInfoUtils::GetNTMajorVersion()
{
OSVERSIONINFOEX osvi;
BOOL bOsVersionInfoEx;
ZeroMemory(&osvi, sizeof(OSVERSIONINFOEX));
osvi.dwOSVersionInfoSize = sizeof(OSVERSIONINFOEX);
bOsVersionInfoEx = GetVersionEx ((OSVERSIONINFO *) &osvi);
if( bOsVersionInfoEx == 0 )
{
osvi.dwOSVersionInfoSize = sizeof (OSVERSIONINFO);
if (! GetVersionEx ( (OSVERSIONINFO *) &osvi) ) 
return FALSE;
}
return osvi.dwMajorVersion;
}
INtDll::PNtQuerySystemInformation INtDll::NtQuerySystemInformation = NULL;
INtDll::PNtQueryObject INtDll::NtQueryObject = NULL;
INtDll::PNtQueryInformationThread	INtDll::NtQueryInformationThread = NULL;
INtDll::PNtQueryInformationFile	INtDll::NtQueryInformationFile = NULL;
INtDll::PNtQueryInformationProcess INtDll::NtQueryInformationProcess = NULL;
DWORD INtDll::dwNTMajorVersion = SystemInfoUtils::GetNTMajorVersion();
BOOL INtDll::NtDllStatus = INtDll::Init();
BOOL INtDll::Init()
{
NtQuerySystemInformation = (PNtQuerySystemInformation)
GetProcAddress( GetModuleHandle( _T( "ntdll.dll" ) ),
_T("NtQuerySystemInformation") );
NtQueryObject = (PNtQueryObject)
GetProcAddress(	GetModuleHandle( _T( "ntdll.dll" ) ),
_T("NtQueryObject") );
NtQueryInformationThread = (PNtQueryInformationThread)
GetProcAddress(	GetModuleHandle( _T( "ntdll.dll" ) ),
_T("NtQueryInformationThread") );
NtQueryInformationFile = (PNtQueryInformationFile)
GetProcAddress(	GetModuleHandle( _T( "ntdll.dll" ) ),
_T("NtQueryInformationFile") );
NtQueryInformationProcess = (PNtQueryInformationProcess)
GetProcAddress(	GetModuleHandle( _T( "ntdll.dll" ) ),
_T("NtQueryInformationProcess") );
return  NtQuerySystemInformation	!= NULL &&
NtQueryObject				!= NULL &&
NtQueryInformationThread	!= NULL &&
NtQueryInformationFile		!= NULL &&
NtQueryInformationProcess	!= NULL;
}
SystemProcessInformation::SystemProcessInformation( BOOL bRefresh )
{
m_pBuffer = (UCHAR*)VirtualAlloc ((void*)0x100000,
BufferSize, 
MEM_COMMIT,
PAGE_READWRITE);
if ( bRefresh )
Refresh();
}
SystemProcessInformation::~SystemProcessInformation()
{
VirtualFree( m_pBuffer, 0, MEM_RELEASE );
}
BOOL SystemProcessInformation::Refresh()
{
m_ProcessInfos.clear();
m_pCurrentProcessInfo = NULL;
if ( !NtDllStatus || m_pBuffer == NULL )
return FALSE;
if ( INtDll::NtQuerySystemInformation( 5, m_pBuffer, BufferSize, NULL )
!= 0 )
return FALSE;
DWORD currentProcessID = GetCurrentProcessId(); //Current Process ID
SYSTEM_PROCESS_INFORMATION* pSysProcess =
(SYSTEM_PROCESS_INFORMATION*)m_pBuffer;
do 
{
m_ProcessInfos[pSysProcess->dUniqueProcessId] = pSysProcess;
if ( pSysProcess->dUniqueProcessId == currentProcessID )
m_pCurrentProcessInfo = pSysProcess;
if ( pSysProcess->dNext != 0 )
pSysProcess = (SYSTEM_PROCESS_INFORMATION*)
((UCHAR*)pSysProcess + pSysProcess->dNext);
else
pSysProcess = NULL;
} while ( pSysProcess != NULL );
return TRUE;
}
SystemThreadInformation::SystemThreadInformation( DWORD pID, BOOL bRefresh )
{
m_processId = pID;
if ( bRefresh )
Refresh();
}
BOOL SystemThreadInformation::Refresh()
{
SystemHandleInformation hi( m_processId );
BOOL rc = hi.SetFilter( _T("Thread"), TRUE );
```, ```
m_ThreadInfos.clear();
if ( !rc )
return FALSE;
THREAD_INFORMATION ti;
for (list<SystemHandleInformation::SYSTEM_HANDLE>::iterator iter = hi.m_HandleInfos.begin(); iter != hi.m_HandleInfos.end(); iter++) {
SystemHandleInformation::SYSTEM_HANDLE& h = *iter;
ti.ProcessId = h.ProcessID;
ti.ThreadHandle = (HANDLE)h.HandleNumber;
if ( SystemHandleInformation::GetThreadId( ti.ThreadHandle,
ti.ThreadId, ti.ProcessId ) )
m_ThreadInfos.push_back( ti );
}
return TRUE;
}
SystemHandleInformation::SystemHandleInformation( DWORD pID, BOOL bRefresh,
LPCTSTR lpTypeFilter )
{
m_processId = pID;
SetFilter( lpTypeFilter, bRefresh );
}
SystemHandleInformation::~SystemHandleInformation()
{
}
BOOL SystemHandleInformation::SetFilter( LPCTSTR lpTypeFilter, BOOL bRefresh )
{
m_strTypeFilter = lpTypeFilter == NULL ? _T("") : lpTypeFilter;
return bRefresh ? Refresh() : TRUE;
}
const string& SystemHandleInformation::GetFilter()
{
return m_strTypeFilter;
}

BOOL SystemHandleInformation::IsSupportedHandle( SYSTEM_HANDLE& handle )
if ( dwNTMajorVersion >= 5 )
return TRUE;
if ( handle.ProcessID == 2 && handle.HandleType == 16 )
return FALSE;
return TRUE;
}
BOOL SystemHandleInformation::Refresh()
{
DWORD size = 0x2000;
DWORD needed = 0;
DWORD i = 0;
BOOL  ret = TRUE;
string strType;
m_HandleInfos.clear();
if ( !INtDll::NtDllStatus )
return FALSE;
SYSTEM_HANDLE_INFORMATION* pSysHandleInformation =
(SYSTEM_HANDLE_INFORMATION*)
VirtualAlloc( NULL, size, MEM_COMMIT, PAGE_READWRITE );
if ( pSysHandleInformation == NULL )
return FALSE;
if ( INtDll::NtQuerySystemInformation( 16, pSysHandleInformation,
size, &needed ) != 0 )
{
if ( needed == 0 )
{
ret = FALSE;
goto cleanup;
VirtualFree( pSysHandleInformation, 0, MEM_RELEASE );
pSysHandleInformation = (SYSTEM_HANDLE_INFORMATION*)
VirtualAlloc( NULL, size = needed + 256,
MEM_COMMIT, PAGE_READWRITE );
}
if ( pSysHandleInformation == NULL )
return FALSE;
if ( INtDll::NtQuerySystemInformation( 16, pSysHandleInformation,
size, NULL ) != 0 )
{
ret = FALSE;
goto cleanup;
}
for ( i = 0; i < pSysHandleInformation->Count; i++ )
{
if ( !IsSupportedHandle( pSysHandleInformation->Handles[i] ) )
continue;
if ( pSysHandleInformation->Handles[i].ProcessID ==
m_processId || m_processId == (DWORD)-1 ) {
BOOL bAdd = FALSE;
if ( m_strTypeFilter == _T("") )
bAdd = TRUE;
else
{
GetTypeToken( (HANDLE)pSysHandleInformation
->Handles[i].HandleNumber,
strType,
pSysHandleInformation
->Handles[i].ProcessID);
bAdd = strType == m_strTypeFilter;
}
if ( bAdd )
{	
pSysHandleInformation->Handles[i].HandleType =
(WORD)(pSysHandleInformation
->Handles[i].HandleType % 256);
m_HandleInfos.push_back( pSysHandleInformation
->Handles[i] );
}
}
}
cleanup:
if ( pSysHandleInformation != NULL )
VirtualFree( pSysHandleInformation, 0, MEM_RELEASE );
return ret;
}
HANDLE SystemHandleInformation::OpenProcess( DWORD processId )
{
return ::OpenProcess( PROCESS_DUP_HANDLE, TRUE, processId );
}
HANDLE SystemHandleInformation::DuplicateHandle( HANDLE hProcess,
HANDLE hRemote )
{
HANDLE hDup = NULL;
::DuplicateHandle( hProcess, hRemote,	GetCurrentProcess(), &hDup,
0, FALSE, DUPLICATE_SAME_ACCESS );
return hDup;
}
BOOL SystemHandleInformation::GetTypeToken( HANDLE h, string& str,
DWORD processId )
{
ULONG size = 0x2000;
UCHAR* lpBuffer = NULL;
BOOL ret = FALSE;
HANDLE handle;
HANDLE hRemoteProcess = NULL;
BOOL remote = processId != GetCurrentProcessId();
if ( !NtDllStatus )
return FALSE;
if ( remote )
{
hRemoteProcess = OpenProcess( processId );
```,
```
if ( hRemoteProcess == NULL )
return FALSE;
handle = DuplicateHandle( hRemoteProcess, h );
}
else
handle = h;
INtDll::NtQueryObject( handle, 2, NULL, 0, &size );
lpBuffer = new UCHAR[size];
if ( INtDll::NtQueryObject( handle, 2, lpBuffer, size, NULL ) == 0 )
{
str = _T("");
SystemInfoUtils::LPCWSTR2string( (LPCWSTR)(lpBuffer+0x60),
str );
ret = TRUE;
}
if ( remote )
{
if ( hRemoteProcess != NULL )
CloseHandle( hRemoteProcess );
if ( handle != NULL )
CloseHandle( handle );
}
if ( lpBuffer != NULL )
delete [] lpBuffer;
return ret;
}
BOOL SystemHandleInformation::GetType( HANDLE h, WORD& type, DWORD processId )
{
string strType;
type = OB_TYPE_UNKNOWN;
if ( !GetTypeToken( h, strType, processId ) )
return FALSE;
return GetTypeFromTypeToken( strType.c_str(), type );
}
BOOL SystemHandleInformation::GetTypeFromTypeToken( LPCTSTR typeToken,
WORD& type )
{
const WORD count = 27;
string constStrTypes[count] = { 
_T(""), _T(""), _T("Directory"), _T("SymbolicLink"),
_T("Token"), _T("Process"), _T("Thread"), _T("Unknown7"),
_T("Event"), _T("EventPair"), _T("Mutant"), _T("Unknown11"),
_T("Semaphore"), _T("Timer"), _T("Profile"),
_T("WindowStation"), _T("Desktop"), _T("Section"), _T("Key"),
_T("Port"), _T("WaitablePort"), _T("Unknown21"),
_T("Unknown22"), _T("Unknown23"), _T("Unknown24"),
_T("IoCompletion"), _T("File") };
type = OB_TYPE_UNKNOWN;
for ( WORD i = 1; i < count; i++ )
if ( constStrTypes[i] == typeToken )
{
type = i;
return TRUE;
}
return FALSE;
}
BOOL SystemHandleInformation::GetName( HANDLE handle, string& str, DWORD processId )
{
WORD type = 0;
if ( !GetType( handle, type, processId  ) )
return FALSE;
return GetNameByType( handle, type, str, processId );
}
BOOL SystemHandleInformation::GetNameByType( HANDLE h, WORD type, string& str, DWORD processId )
{
ULONG size = 0x2000;
UCHAR* lpBuffer = NULL;
BOOL ret = FALSE;
HANDLE handle;
HANDLE hRemoteProcess = NULL;
BOOL remote = processId != GetCurrentProcessId();
DWORD dwId = 0;
if ( !NtDllStatus )
return FALSE;
if ( remote )
{
hRemoteProcess = OpenProcess( processId );
if ( hRemoteProcess == NULL )
return FALSE;
handle = DuplicateHandle( hRemoteProcess, h );
}
else
handle = h;
stringstream hex;
switch( type )
{
case OB_TYPE_PROCESS:
GetProcessId( handle, dwId );
hex << "PID: 0x" << std::hex << dwId;
str = hex.str();
ret = TRUE;
goto cleanup;
break;
case OB_TYPE_THREAD:
GetThreadId( handle, dwId );
hex << "TID: 0x" << std::hex << dwId;
ret = TRUE;
goto cleanup;
break;
case OB_TYPE_FILE:
ret = GetFileName( handle, str );
if ( ret && str == _T("") )
goto cleanup;
break;
};
INtDll::NtQueryObject ( handle, 1, NULL, 0, &size );
if ( size == 0 )
size = 0x2000;
lpBuffer = new UCHAR[size];
if ( INtDll::NtQueryObject( handle, 1, lpBuffer, size, NULL ) == 0 )
{
SystemInfoUtils::Unicode2string( (UNICODE_STRING*)lpBuffer, str );
ret = TRUE;
}
cleanup:
if ( remote )
{
if ( hRemoteProcess != NULL )
CloseHandle( hRemoteProcess );
if ( handle != NULL )
CloseHandle( handle );
}
if ( lpBuffer != NULL )
delete [] lpBuffer;
return ret;
}
BOOL SystemHandleInformation::GetThreadId( HANDLE h, DWORD& threadID, DWORD processId )
{
SystemThreadInformation::BASIC_THREAD_INFORMATION ti;
HANDLE handle;
HANDLE hRemoteProcess = NULL;
BOOL remote = processId != GetCurrentProcessId();
if ( !NtDllStatus )
return FALSE;
if ( remote )
{
hRemoteProcess = OpenProcess( processId );
if ( hRemoteProcess == NULL )
return FALSE;
handle = DuplicateHandle( hRemoteProcess, h );
}
else
handle = h;
if ( INtDll::NtQueryInformationThread( handle, 0, &ti, sizeof(ti), NULL ) == 0 )
threadID = ti.ThreadId;
if ( remote )
{
if ( hRemoteProcess != NULL )
CloseHandle( hRemoteProcess );
if ( handle != NULL )
CloseHandle( handle );
}
return TRUE;
}
BOOL SystemHandleInformation::GetProcessPath( HANDLE h, string& strPath, DWORD remoteProcessId )
{
h; strPath; remoteProcessId;
stringstream number;
number << remoteProcessId;
strPath = number.str();
return TRUE;
}
BOOL SystemHandleInformation::GetProcessId( HANDLE h, DWORD& processId, DWORD remoteProcessId )
{
BOOL ret = FALSE;
HANDLE handle;
HANDLE hRemoteProcess = NULL;
BOOL remote = remoteProcessId != GetCurrentProcessId();
SystemProcessInformation::PROCESS_BASIC_INFORMATION pi;
ZeroMemory( &pi, sizeof(pi) );
processId = 0;
if ( !NtDllStatus )
return FALSE;
if ( remote )
{
hRemoteProcess = OpenProcess( remoteProcessId );
if ( hRemoteProcess == NULL )
return FALSE;
handle = DuplicateHandle( hRemoteProcess, h );
}
else
handle = h;
if ( INtDll::NtQueryInformationProcess( handle, 0, &pi, sizeof(pi), NULL) == 0 )
{
processId = pi.UniqueProcessId;
ret = TRUE;
}
if ( remote )
{
if ( hRemoteProcess != NULL )
CloseHandle( hRemoteProcess );
if ( handle != NULL )
CloseHandle( handle );
}
return ret;
}
void SystemHandleInformation::GetFileNameThread( PVOID pParam )
{
GetFileNameThreadParam* p = (GetFileNameThreadParam*)pParam;
UCHAR lpBuffer[0x1000];
DWORD iob[2];
p->rc = INtDll::NtQueryInformationFile( p->hFile, iob, lpBuffer, sizeof(lpBuffer), 9 );
if ( p->rc == 0 )
*p->pName = (const char *)lpBuffer;
}
BOOL SystemHandleInformation::GetFileName( HANDLE h, string& str, DWORD processId )
{
BOOL ret= FALSE;
HANDLE hThread = NULL;
GetFileNameThreadParam tp;
HANDLE handle;
HANDLE hRemoteProcess = NULL;
BOOL remote = processId != GetCurrentProcessId();
if ( !NtDllStatus )
return FALSE;
if ( remote )
{
hRemoteProcess = OpenProcess( processId );
if ( hRemoteProcess == NULL )
return FALSE;
handle = DuplicateHandle( hRemoteProcess, h );
}
else
handle = h;
tp.hFile = handle;
tp.pName = &str;
tp.rc = 0;
hThread = (HANDLE)_beginthread( GetFileNameThread, 0, &tp );
if ( hThread == NULL )
{
ret = FALSE;
goto cleanup;
}
if ( WaitForSingleObject( hThread, 100 ) == WAIT_TIMEOUT )
{
TerminateThread( hThread, 0 );
str = _T("");
ret = TRUE;
}
else
ret = ( tp.rc == 0 );
cleanup:
if ( remote )
{
if ( hRemoteProcess != NULL )
CloseHandle( hRemoteProcess );
if ( handle != NULL )
CloseHandle( handle );
}
return ret;
}
```,
```
SystemModuleInformation::SystemModuleInformation( DWORD pID, BOOL bRefresh )
{
m_processId = pID;
if ( bRefresh )
Refresh();
void SystemModuleInformation::GetModuleListForProcess( DWORD processID )
{
DWORD i = 0;
DWORD cbNeeded = 0;
HMODULE* hModules = NULL;
MODULE_INFO moduleInfo;
HANDLE hProcess = OpenProcess( PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, processID );
if ( hProcess == NULL )
goto cleanup;
if ( !(*m_EnumProcessModules)( hProcess, NULL, 0, &cbNeeded ) )
goto cleanup;
hModules = new HMODULE[ cbNeeded / sizeof( HMODULE ) ];
if ( !(*m_EnumProcessModules)( hProcess, hModules, cbNeeded, &cbNeeded ) )
goto cleanup;
for ( i = 0; i < cbNeeded / sizeof( HMODULE ); i++ )
{
moduleInfo.ProcessId = processID;
moduleInfo.Handle = hModules[i];
if ( (*m_GetModuleFileNameEx)( hProcess, hModules[i], moduleInfo.FullPath, _MAX_PATH ) )
m_ModuleInfos.push_back( moduleInfo );
}
cleanup:
if ( hModules != NULL )
delete [] hModules;
if ( hProcess != NULL )
CloseHandle( hProcess );
}
BOOL SystemModuleInformation::Refresh()
{
BOOL rc = FALSE;
m_EnumProcessModules = NULL;
m_GetModuleFileNameEx = NULL;
m_ModuleInfos.clear();
HINSTANCE hDll = LoadLibrary( "PSAPI.DLL" );
if ( hDll == NULL )
{
rc = FALSE;
goto cleanup;
}
m_EnumProcessModules = (PEnumProcessModules)GetProcAddress( hDll, "EnumProcessModules" );
m_GetModuleFileNameEx = (PGetModuleFileNameEx)GetProcAddress( hDll, 
#ifdef UNICODE
"GetModuleFileNameExW" );
#else
"GetModuleFileNameExA" );
#endif
if ( m_GetModuleFileNameEx == NULL || m_EnumProcessModules == NULL )
{
rc = FALSE;
goto cleanup;
}
if ( m_processId != -1 )
GetModuleListForProcess( m_processId );
else
{
DWORD pID;
SystemProcessInformation::SYSTEM_PROCESS_INFORMATION* p = NULL;
SystemProcessInformation pi( TRUE );
if ( pi.m_ProcessInfos.empty() )
{
rc = FALSE;
goto cleanup;
};''']  # code_cpp
        code_python = [
            '''__all__ = ['tqdm', 'trange']
import sys
import time
def format_interval(t):
mins, s = divmod(int(t), 60)
h, m = divmod(mins, 60)
if h:
return '%d:%02d:%02d' % (h, m, s)
else:
return '%02d:%02d' % (m, s)
def format_meter(n, total, elapsed):
if n > total:
total = None
elapsed_str = format_interval(elapsed)
rate = '%5.2f' % (n / elapsed) if elapsed else '?'
if total:
frac = float(n) / total
N_BARS = 10
bar_length = int(frac*N_BARS)
bar = '#'*bar_length + '-'*(N_BARS-bar_length)
percentage = '%3d%%' % (frac * 100)
left_str = format_interval(elapsed / n * (total-n)) if n else '?'
return '|%s| %d/%d %s [elapsed: %s left: %s, %s iters/sec]' % (
bar, n, total, percentage, elapsed_str, left_str, rate)
else:
return '%d [elapsed: %s, %s iters/sec]' % (n, elapsed_str, rate)
class StatusPrinter(object):
def __init__(self, file):
self.file = file
self.last_printed_len = 0
def print_status(self, s):
self.file.write('\r'+s+' '*max(self.last_printed_len-len(s), 0))
self.file.flush()
self.last_printed_len = len(s)
def tqdm(iterable, desc='', total=None, leave=False, file=sys.stderr,
mininterval=0.5, miniters=1):
if total is None:
try:
total = len(iterable)
except TypeError:
total = None
prefix = desc+': ' if desc else ''
sp = StatusPrinter(file)
sp.print_status(prefix + format_meter(0, total, 0))
start_t = last_print_t = time.time()
last_print_n = 0
n = 0
for obj in iterable:
yield obj
n += 1
if n - last_print_n >= miniters:
cur_t = time.time()
if cur_t - last_print_t >= mininterval:
sp.print_status(prefix + format_meter(n, total, cur_t-start_t))
last_print_n = n
last_print_t = cur_t
if not leave:
sp.print_status('')
sys.stdout.write('\r')
else:
if last_print_n < n:
cur_t = time.time()
sp.print_status(prefix + format_meter(n, total, cur_t-start_t))
file.write('\n')
def trange(*args, **kwargs):
try:
f = xrange
except NameError:
f = range
return tqdm(f(*args), **kwargs)''',
'''#!/usr/bin/python
import os
import sys
import logging
import time
from threading import Thread
from queue import Queue, Empty
from enum import Enum
sys.path.append('.')
from pogom.schedulers import KeyScheduler
from pogom.account import (check_login, setup_api, pokestop_spinnable,
spin_pokestop, TooManyLoginAttempts)
from pogom.utils import get_args, gmaps_reverse_geolocate
from pogom.apiRequests import (get_map_objects as gmo,
AccountBannedException)
from runserver import (set_log_and_verbosity, startup_db,
class FakeQueue:
def put(self, something):
pass
class ErrorType(Enum):
generic = 1
captcha = 2
no_stops = 3
banned = 4
login_error = 5
def get_location_forts(api, account, location):
response = gmo(api, account, location)
if len(response['responses']['CHECK_CHALLENGE'].challenge_url) > 1:
log.error('account: %s got captcha: %s', account['username'],
response['responses']['CHECK_CHALLENGE'].challenge_url)
return (ErrorType.captcha, None)
cells = response['responses']['GET_MAP_OBJECTS'].map_cells
forts = []
for cell in cells:
for fort in cell.forts:
if fort.type == 1:
forts.append(fort)
if not forts:
return (ErrorType.no_stops, None)
return (None, forts)
def level_up_account(args, location, accounts, errors):
while True:
try:
try:
(account, error_count) = accounts.get(False)
except Empty:
break
log.info('Starting account %s', account['username'])
status = {
'type': 'Worker',
'message': 'Creating thread...',
'success': 0,
'fail': 0,
'noitems': 0,
'skip': 0,
'captcha': 0,
'username': '',
'proxy_display': None,
'proxy_url': None,
}
api = setup_api(args, status, account)
key = key_scheduler.next()
api.set_position(*location)
api.activate_hash_server(key)
check_login(args, account, api, status['proxy_url'])
log.info('Logged in account %s, level %d.', account['username'],
account['level'])
(error, forts) = get_location_forts(api, account, location)
if error:
errors[error].append(account)
accounts.task_done()
continue
spinnable_pokestops = filter(
lambda fort: pokestop_spinnable(fort, location), forts)
first_fort = forts[0]
if not spinnable_pokestops:
log.critical('No Pokestops in spinnable range. Please move'
first_fort.latitude,
first_fort.longitude)
os._exit(1)
fort = spinnable_pokestops[0]
spin_pokestop(api, account, args, fort, location)
''', '''
log.info('Spun Pokestop with account %s, level %d.',
account['username'],
account['level'])
except TooManyLoginAttempts:
errors[ErrorType.login_error].append(account)
except AccountBannedException:
errors[ErrorType.banned].append(account)
except Exception as e:
if error_count < 2:
log.exception('Exception in worker: %s. Retrying.', e)
accounts.put((account, error_count + 1))
else:
errors[ErrorType.generic].append(account)
accounts.task_done()
log = logging.getLogger()
set_log_and_verbosity(log)
args = get_args()
if not args.hash_key:
log.critical('Hashing key is required. Exiting.')
sys.exit(1)
fake_queue = FakeQueue()
key_scheduler = KeyScheduler(args.hash_key, fake_queue)
position = extract_coordinates(args.location)
args.player_locale = PlayerLocale.get_locale(args.location)
if not args.player_locale:
args.player_locale = gmaps_reverse_geolocate(
args.gmaps_key,
args.locale,
str(position[0]) + ', ' + str(position[1]))
startup_db(None, args.clear_db)
initialize_proxies(args)
account_queue = Queue()
errors = {}
for error in ErrorType:
errors[error] = []
for account in args.accounts:
account_queue.put((account, 0))
for i in range(0, args.workers):
log.debug('Starting level-up worker thread %d...', i)
t = Thread(target=level_up_account,
name='worker-{}'.format(i),
args=(args, position, account_queue, errors))
t.daemon = True
t.start()
try:
while True:
if account_queue.unfinished_tasks > 0:
time.sleep(1)
else:
break
except KeyboardInterrupt:
log.info('Process killed.')
exit(1)
account_queue.join()
log.info('Process finished.')
for error_type in ErrorType:
if len(errors[error_type]) > 0:
log.warning('Some accounts did not finish properly (%s):',
error_type.name)
for account in errors[error_type]:
log.warning('\t%s', account['username'])''',
'''from builtins import range
from collections import namedtuple
from datetime import datetime
import csv
import math
import time
import tensorflow.python.platform
import tensorflow as tf
FLAGS = tf.app.flags.FLAGS
parameters = []
conv_counter = 1
pool_counter = 1
affine_counter = 1
TimingEntry = namedtuple(
'TimingEntry', ['info_string', 'timestamp', 'num_batches', 'mean', 'sd'])
def _conv(inpOp, nIn, nOut, kH, kW, dH, dW, padType):
global conv_counter
global parameters
name = 'conv' + str(conv_counter)
conv_counter += 1
with tf.name_scope(name) as scope:
kernel = tf.Variable(tf.truncated_normal([kH, kW, nIn, nOut],
dtype=tf.float32,
stddev=1e-1), name='weights')
if FLAGS.data_format == 'NCHW':
strides = [1, 1, dH, dW]
else:
strides = [1, dH, dW, 1]
conv = tf.nn.conv2d(inpOp, kernel, strides, padding=padType,
data_format=FLAGS.data_format)
biases = tf.Variable(tf.constant(0.0, shape=[nOut], dtype=tf.float32),
trainable=True, name='biases')
bias = tf.reshape(tf.nn.bias_add(conv, biases,
data_format=FLAGS.data_format),
conv.get_shape())
conv1 = tf.nn.relu(bias, name=scope)
parameters += [kernel, biases]
return conv1
def _affine(inpOp, nIn, nOut):
global affine_counter
global parameters
name = 'affine' + str(affine_counter)
affine_counter += 1
with tf.name_scope(name) as scope:
kernel = tf.Variable(tf.truncated_normal([nIn, nOut],
dtype=tf.float32,
stddev=1e-1), name='weights')
biases = tf.Variable(tf.constant(0.0, shape=[nOut], dtype=tf.float32),
trainable=True, name='biases')
affine1 = tf.nn.relu_layer(inpOp, kernel, biases, name=name)
parameters += [kernel, biases]
return affine1
def _mpool(inpOp, kH, kW, dH, dW, padding):
global pool_counter
global parameters
name = 'pool' + str(pool_counter)
pool_counter += 1
if FLAGS.data_format == 'NCHW':
ksize = [1, 1, kH, kW]
strides = [1, 1, dH, dW]
else:
ksize = [1, kH, kW, 1]
strides = [1, dH, dW, 1]
return tf.nn.max_pool(inpOp,
ksize=ksize,
strides=strides,
padding=padding,
data_format=FLAGS.data_format,
name=name)
def _apool(inpOp, kH, kW, dH, dW, padding):
global pool_counter
global parameters
name = 'pool' + str(pool_counter)
pool_counter += 1
if FLAGS.data_format == 'NCHW':
ksize = [1, 1, kH, kW]
strides = [1, 1, dH, dW]
else:
ksize = [1, kH, kW, 1]
strides = [1, dH, dW, 1]
return tf.nn.avg_pool(inpOp,
ksize=ksize,
strides=strides,
padding=padding,
data_format=FLAGS.data_format,
name=name)
def _inception(inp, inSize, o1s, o2s1, o2s2, o3s1, o3s2, o4s1, o4s2):
conv1 = _conv(inp, inSize, o1s, 1, 1, 1, 1, 'SAME')
conv3_ = _conv(inp, inSize, o2s1, 1, 1, 1, 1, 'SAME')
conv3 = _conv(conv3_, o2s1, o2s2, 3, 3, 1, 1, 'SAME')
conv5_ = _conv(inp, inSize, o3s1, 1, 1, 1, 1, 'SAME')
conv5 = _conv(conv5_, o3s1, o3s2, 5, 5, 1, 1, 'SAME')
pool_ = _mpool(inp, o4s1, o4s1, 1, 1, 'SAME')
pool = _conv(pool_, inSize, o4s2, 1, 1, 1, 1, 'SAME')
if FLAGS.data_format == 'NCHW':
channel_dim = 1
else:
channel_dim = 3
incept = tf.concat([conv1, conv3, conv5, pool], channel_dim)
return incept
def loss(logits, labels):
batch_size = tf.size(labels)
labels = tf.expand_dims(labels, 1)
indices = tf.expand_dims(tf.range(0, batch_size, 1), 1)
concated = tf.concat([indices, labels], 1)
onehot_labels = tf.sparse_to_dense(
concated, tf.stack([batch_size, 1000]), 1.0, 0.0)
cross_entropy = tf.nn.softmax_cross_entropy_with_logits(
logits=logits, labels=onehot_labels, name='xentropy')
loss = tf.reduce_mean(cross_entropy, name='xentropy_mean')
return loss
def inference(images):
conv1 = _conv (images, 3, 64, 7, 7, 2, 2, 'SAME')
pool1 = _mpool(conv1,  3, 3, 2, 2, 'SAME')
conv2 = _conv (pool1,  64, 64, 1, 1, 1, 1, 'SAME')
conv3 = _conv (conv2,  64, 192, 3, 3, 1, 1, 'SAME')
pool3 = _mpool(conv3,  3, 3, 2, 2, 'SAME')
incept3a = _inception(pool3,    192, 64, 96, 128, 16, 32, 3, 32)
incept3b = _inception(incept3a, 256, 128, 128, 192, 32, 96, 3, 64)
pool4 = _mpool(incept3b,  3, 3, 2, 2, 'SAME')
incept4a = _inception(pool4,    480, 192,  96, 208, 16, 48, 3, 64)
incept4b = _inception(incept4a, 512, 160, 112, 224, 24, 64, 3, 64)
incept4c = _inception(incept4b, 512, 128, 128, 256, 24, 64, 3, 64)
incept4d = _inception(incept4c, 512, 112, 144, 288, 32, 64, 3, 64)
incept4e = _inception(incept4d, 528, 256, 160, 320, 32, 128, 3, 128)
pool5 = _mpool(incept4e,  3, 3, 2, 2, 'SAME')
incept5a = _inception(pool5,    832, 256, 160, 320, 32, 128, 3, 128)
incept5b = _inception(incept5a, 832, 384, 192, 384, 48, 128, 3, 128)
pool6 = _apool(incept5b,  7, 7, 1, 1, 'VALID')
resh1 = tf.reshape(pool6, [-1, 1024])
affn1 = _affine(resh1, 1024, 1000)
return affn1
'''] # code_python
        code_javascript = [
            '''(function(root, factory) {
if (typeof define === 'function' && define.amd) {
define('gridster-coords', ['jquery'], factory);
} else {
root.GridsterCoords = factory(root.$ || root.jQuery);
}
}(this, function($) {
function Coords(obj) {
if (obj[0] && $.isPlainObject(obj[0])) {
this.data = obj[0];
}else {
this.el = obj;
}
this.isCoords = true;
this.coords = {};
this.init();
return this;
}
var fn = Coords.prototype;
fn.init = function(){
this.set();
this.original_coords = this.get();
};
fn.set = function(update, not_update_offsets) {
var el = this.el;
if (el && !update) {
this.data = el.offset();
this.data.width = el.width();
this.data.height = el.height();
}
if (el && update && !not_update_offsets) {
var offset = el.offset();
this.data.top = offset.top;
this.data.left = offset.left;
}
var d = this.data;
typeof d.left === 'undefined' && (d.left = d.x1);
typeof d.top === 'undefined' && (d.top = d.y1);
this.coords.x1 = d.left;
this.coords.y1 = d.top;
this.coords.x2 = d.left + d.width;
this.coords.y2 = d.top + d.height;
this.coords.cx = d.left + (d.width / 2);
this.coords.cy = d.top + (d.height / 2);
this.coords.width  = d.width;
this.coords.height = d.height;
this.coords.el  = el || false ;
return this;
};
fn.update = function(data){
if (!data && !this.el) {
return this;
}
if (data) {
var new_data = $.extend({}, this.data, data);
this.data = new_data;
return this.set(true, true);
}
this.set(true);
return this;
};
fn.get = function(){
return this.coords;
};
fn.destroy = function() {
this.el.removeData('coords');
delete this.el;
};
$.fn.coords = function() {
if (this.data('coords') ) {
return this.data('coords');
}
var ins = new Coords(this, arguments[0]);
this.data('coords', ins);
return ins;
};
return Coords;
}));''',
'''(function (win, undefined) {
"use strict";
var doc = win.document,
domWaiters = [],
queue      = [], // waiters for the "head ready" event
handlers   = {}, // user functions waiting for events
assets     = {}, // loadable items in various states
isAsync    = "async" in doc.createElement("script") || "MozAppearance" in doc.documentElement.style || win.opera,
isHeadReady,
isDomReady,
api.ready.apply(null, arguments);
}),
PRELOADING = 1,
PRELOADED  = 2,
LOADING    = 3,
LOADED     = 4;
function each(arr, callback) {
if (!arr) {
return;
}
if (typeof arr === "object") {
arr = [].slice.call(arr);
}
for (var i = 0, l = arr.length; i < l; i++) {
callback.call(arr, arr[i], i);
}
}
function is(type, obj) {
var clas = Object.prototype.toString.call(obj).slice(8, -1);
return obj !== undefined && obj !== null && clas === type;
}
function isFunction(item) {
return is("Function", item);
}
function isArray(item) {
return is("Array", item);
}
return i !== -1 ? name.substring(0, i) : name;
}
function one(callback) {
callback = callback || noop;
if (callback._done) {
return;
}
callback();
callback._done = 1;
}
function conditional(test, success, failure, callback) {
var obj = (typeof test === "object") ? test : {
test: test,
success: !!success ? isArray(success) ? success : [success] : false,
failure: !!failure ? isArray(failure) ? failure : [failure] : false,
callback: callback || noop
};
var passed = !!obj.test;
if (passed && !!obj.success) {
obj.success.push(obj.callback);
api.load.apply(null, obj.success);
}
else if (!passed && !!obj.failure) {
obj.failure.push(obj.callback);
api.load.apply(null, obj.failure);
}
else {
callback();
}
return api;
var asset = {};
if (typeof item === "object") {
for (var label in item) {
if (!!item[label]) {
asset = {
name: label,
url : item[label]
};
}
}
}
else {
asset = {
name: toLabel(item),
url : item
};
}
var existing = assets[asset.name];
if (existing && existing.url === asset.url) {
return existing;
}
assets[asset.name] = asset;
return asset;
}
function allLoaded(items) {
items = items || assets;
for (var name in items) {
if (items.hasOwnProperty(name) && items[name].state !== LOADED) {
return false;
}
}
function onPreload(asset) {
asset.state = PRELOADED;
each(asset.onpreload, function (afterPreload) {
afterPreload.call();
});
}
''',
'''
function preLoad(asset, callback) {
if (asset.state === undefined) {
asset.state     = PRELOADING;
asset.onpreload = [];
var args = arguments,
rest = [].slice.call(args, 1),
next = rest[0];
if (!isHeadReady) {
queue.push(function () {
api.load.apply(null, args);
});
return api;
}
each(rest, function (item) {
if (!isFunction(item) && !!item) {
preLoad(getAsset(item));
}
});
load(getAsset(args[0]), isFunction(next) ? next : function () {
api.load.apply(null, rest);
});
}
else {
load(getAsset(args[0]));
}
return api;
}
function apiLoadAsync() {
callback = args[args.length - 1],
items    = {};
if (!isFunction(callback)) {
callback = null;
}
if (isArray(args[0])) {
args[0].push(callback);
api.load.apply(null, args[0]);
return api;
}
each(args, function (item, i) {
if (item !== callback) {
item             = getAsset(item);
items[item.name] = item;
}
});
each(args, function (item, i) {
if (item !== callback) {
item = getAsset(item);
load(item, function () {
if (allLoaded(items)) {
one(callback);
}
});
}
});
return api;
}
function load(asset, callback) {
callback = callback || noop;
if (asset.state === LOADED) {
callback();
return;
}
if (asset.state === LOADING) {
api.ready(asset.name, callback);
return;
}
if (asset.state === PRELOADING) {
asset.onpreload.push(function () {
load(asset, callback);
});
return;
}
asset.state = LOADING;
loadAsset(asset, function () {
asset.state = LOADED;
callback();
''',
'''
each(handlers[asset.name], function (fn) {
one(fn);
});
if (isDomReady && allLoaded()) {
each(handlers.ALL, function (fn) {
one(fn);
});
}
});
}
function loadAsset(asset, callback) {
callback = callback || noop;
function error(event) {
event = event || win.event;
ele.onload = ele.onreadystatechange = ele.onerror = null;
callback();
}
function process(event) {
ele.onload = ele.onreadystatechange = ele.onerror = null;
callback();
}
}

var ele;
if (/\.css[^\.]*$/.test(asset.url)) {
ele      = doc.createElement("link");
ele.type = "text/" + (asset.type || "css");
ele.rel  = "stylesheet";
ele.href = asset.url;
}
else {
ele      = doc.createElement("script");
ele.type = "text/" + (asset.type || "javascript");
ele.src  = asset.url;
}
ele.onload  = ele.onreadystatechange = process;
ele.onerror = error;
ele.async = false;
ele.defer = false;
var head = doc.head || doc.getElementsByTagName("head")[0];
head.insertBefore(ele, head.lastChild);
}
function init() {
var items = doc.getElementsByTagName("script");
for (var i = 0, l = items.length; i < l; i++) {
var dataMain = items[i].getAttribute("data-headjs-load");
if (!!dataMain) {
api.load(dataMain);
return;
}
}
}
function ready(key, callback) {
if (key === doc) {
if (isDomReady) {
one(callback);
}
else {
domWaiters.push(callback);
}
return api;
}
if (isFunction(key)) {
callback = key;
}
if (isArray(key)) {
var items = {};
each(key, function (item) {
items[item] = assets[item];
api.ready(item, function() {
if (allLoaded(items)) {
one(callback);
}
});
});
return api;
}
if (typeof key !== "string" || !isFunction(callback)) {
return api;
}
var asset = assets[key];
if (asset && asset.state === LOADED || key === "ALL" && allLoaded() && isDomReady) {
one(callback);
return api;
}
var arr = handlers[key];
if (!arr) {
arr = handlers[key] = [callback];
}
else {
arr.push(callback);
}
return api;
}
function domReady() {
if (!doc.body) {
win.clearTimeout(api.readyTimeout);
api.readyTimeout = win.setTimeout(domReady, 50);
return;
}
if (!isDomReady) {
isDomReady = true;
init();
each(domWaiters, function (fn) {
one(fn);
});
}
}
''',
'''
function domContentLoaded() {
if (doc.addEventListener) {
doc.removeEventListener("DOMContentLoaded", domContentLoaded, false);
domReady();
}
if (doc.readyState === "complete") {
domReady();
}
else if (doc.addEventListener) {
doc.addEventListener("DOMContentLoaded", domContentLoaded, false);
win.addEventListener("load", domReady, false);
}
else {
doc.attachEvent("onreadystatechange", domContentLoaded);
win.attachEvent("onload", domReady);
var top = false;
try {
top = !win.frameElement && doc.documentElement;
} catch (e) { }
if (top && top.doScroll) {
(function doScrollCheck() {
if (!isDomReady) {
try {
top.doScroll("left");
} catch (error) {
win.clearTimeout(api.readyTimeout);
api.readyTimeout = win.setTimeout(doScrollCheck, 50);
return;
}
domReady();
}
}());
}
}
api.load = api.js = isAsync ? apiLoadAsync : apiLoadHack;
api.test = conditional;
api.ready = ready;
api.ready(doc, function () {
if (isHeadReady && allLoaded()) {
each(handlers.ALL, function (callback) {
one(callback);
});
}
if (api.feature) {
api.feature("domloaded", true);
}
});
setTimeout(function () {
isHeadReady = true;
each(queue, function (fn) {
fn();
});
}, 300);
}(window));''']  # code_javascript
        code_html = [
'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" 
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
<title>script.aculo.us functional tests</title>
</head>
<frameset cols="250,*">
<frame name="controls" src="functional/index.html" />
<frame name="test" />
</frameset>
<noframes>
<body>
Heya, 1995!
</body>
</noframes>
</html>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" 
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
<title>script.aculo.us Unit Test Runner</title>
</head>
<frameset cols="250,*">
<frame name="controls" src="unit/index.html" />
<frame name="test" />
</frameset>
<noframes>
<body>
Heya, 1995!
</body>
</noframes>
</html>''',
'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>script.aculo.us Unit test file</title>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<script src="../../lib/prototype.js" type="text/javascript"></script>
<script src="../../src/scriptaculous.js" type="text/javascript"></script>
<script src="../../src/unittest.js" type="text/javascript"></script>
<link rel="stylesheet" href="../test.css" type="text/css" />
</head>
<body>
<p>
</p>
<div id="testlog"> </div>
<div id="result"></div>
<script type="text/javascript" language="javascript" charset="utf-8">
</script>
</body>
</html>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>script.aculo.us Unit test file</title>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<script src="../../lib/prototype.js" type="text/javascript"></script>
<script src="../../src/scriptaculous.js" type="text/javascript"></script>
<script src="../../src/unittest.js" type="text/javascript"></script>
<link rel="stylesheet" href="../test.css" type="text/css" />
</head>
<body class="navigation">
<h1>script.aculo.us<br/>Unit Tests</h1>
<p id="version"></p>
<script type="text/javascript" language="javascript" charset="utf-8">
</script>
<h2>scriptaculous.js</h2>
<ul>
<li><a href="loading_test.html" target="test">Dynamic loading test</a></li>
</ul>
<ul>
<li><a href="effects_test.html" target="test">Effects test</a></li>
<li><a href="string_test.html" target="test">String test</a></li>
<li><a href="element_test.html" target="test">Element extensions test</a></li>
<li><a href="position_clone_test.html" target="test">Position.clone test</a></li>
</ul>
<h2>dragdrop.js</h2>
<ul>
<li><a href="dragdrop_test.html" target="test">Drag &amp; Drop test</a></li>
<li><a href="sortable_test.html" target="test">Sortable test</a></li>
</ul>
<h2>builder.js</h2>
<ul>
<li><a href="builder_test.html" target="test">Builder test</a></li>
</ul>
<h2>controls.js</h2>
<ul>
<li><a href="ajax_autocompleter_test.html" target="test">Ajax.Autocompleter test</a></li>
<li><a href="ajax_inplaceeditor_test.html" target="test">Ajax.InPlaceEditor test</a></li>
<li>Note: unit tests work on Firefox only. The controls themselves are fully supported on IE6+, Firefox and Safari.</li>
</ul>
<ul>
<li><a href="slider_test.html" target="test">Control.Slider test</a></li>
</ul>
<ul>
<li><a href="unittest_test.html" target="test">Unittest test</a></li>
<li><a href="bdd_test.html" target="test">BDD test</a></li>
</ul>
</body>
</html>''']  # code_html
        code_css = [
            '''@if $use-matrix == true{
<ul class="matrix  three-cols">
<li class=all-cols>Lorem</li>
<li>Ipsum <a href=#>dolor</a></li>
<li><a href=# class=matrix__link>Sit</a></li>
<li>Amet</li>
<li class=all-cols>Consectetuer</li>
</ul>
.matrix{
@extend .block-list;
border-left-width:1px;
@extend .cf;
> li{
float:left;
border-right-width:1px;
@if $global-border-box == false{
@include vendor(box-sizing, border-box);
}
}
}
.matrix__link{
@extend .block-list__link;
}
<ul class="multi-list  four-cols">
<li>Lorem</li>
<li>Ipsum</li>
<li>Dolor</li>
<li>Sit</li>
</ul>
.multi-list{
list-style:none;
margin-left:0;
@extend .cf;
}
.multi-list > li{
float:left;
}
.two-cols > li{
width:50%;
}
.three-cols > li{
width:33.333%;
}
.four-cols > li{
width:25%;
}
.five-cols > li{
width:20%;
}
.matrix > .all-cols,
.multi-list > .all-cols{
width:100%;
}
}//endif''',
'''.button {
font-family: inherit;
text-decoration: none;
cursor: pointer;
border: none;
-webkit-appearance: none;
appearance: none;
white-space: nowrap;
display: inline-block;
line-height: 2rem;
height: auto;
min-height: 2rem;
padding: .5rem 1rem;
.p1  { padding: 1rem; }
.px1 { padding-right: 1rem; padding-left: 1rem; }
.py1 { padding-top: 1rem; padding-bottom: 1rem; }
.p2  { padding: 2rem; }
.px2 { padding-right: 2rem; padding-left: 2rem; }
.py2 { padding-top: 2rem; padding-bottom: 2rem; }
.p3  { padding: 3rem; }
.px3 { padding-right: 3rem; padding-left: 3rem; }
.py3 { padding-top: 3rem; padding-bottom: 3rem; }
.p4  { padding: 4rem; }
.px4 { padding-right: 4rem; padding-left: 4rem; }
.py4 { padding-top: 4rem; padding-bottom: 4rem; }
.p-responsive { padding: 1.5rem; }
.px-responsive { padding-right: 1.5rem; padding-left: 1.5rem; }
.py-responsive { padding-top: 1.5rem; padding-bottom: 1.5rem; }
@media screen and (min-width: 48em) and (max-width: 64em) {
  .p-responsive { padding: 3rem; }
  .px-responsive { padding-right: 3rem; padding-left: 3rem; }
  .py-responsive { padding-top: 3rem; padding-bottom: 3rem; }
}
@media screen and (min-width: 64em) {
  .p-responsive { padding: 4rem; }
  .px-responsive { padding-right: 4rem; padding-left: 4rem; }
  .py-responsive { padding-top: 4rem; padding-bottom: 4rem; }
}
@import "reset";
@import "type";
@import "margins";
@import "padding";
@import "table-object";
@import "utilities";
@import "buttons";
@import "theme";''',
'''.inline{ display: inline; }
.block{ display: block; }
.inline-block { display: inline-block; }
.oh{ overflow: hidden; }
.left{ float: left; }
.right{ float: right; }
.clearfix {
&:before, &:after { content: " "; display: table; }
&:after { clear: both; }
}
.fit { max-width: 100%; }
.full-width { width: 100%; }
.half-width { width: 50%; }
.mobile-show {
display: none;
}
@media screen and (max-width: 48em) {
.mobile-show,
.mobile-block {
display: block;
}
.mobile-block {
width: 100%;
}
.mobile-hide {
display: none;
}
.mobile-center {
text-align: center;
}
}''']  # code_css

        if lang == self.av_langs[0]:
            return code_php
        elif lang == self.av_langs[1]:
            return code_c
        elif lang == self.av_langs[2]:
            return code_cpp
        elif lang == self.av_langs[3]:
            return code_python
        elif lang == self.av_langs[4]:
            return code_javascript
        elif lang == self.av_langs[5]:
            return code_html
        elif lang == self.av_langs[6]:
            return code_css
        else:
            raise ValueError('Неизвестный язык')

            

if __name__ == "__main__":
    clang = CodeLang(argv[1])
    print(clang.run())
