import scrapy
from scrapy.http import FormRequest

class HvaSpider(scrapy.Spider):
    name = 'hva'
    allowed_domains = ['supportsites.husqvarnagroup.com']
    start_urls = ['https://supportsites.husqvarnagroup.com/it']
    login_url = ['https://federate.husqvarnagroup.com/mga/sps/authsvc?PolicyId=urn:ibm:security:authentication:asf:newauthpolicy&TAM_OP=login']

    '''
    <form method="POST" action="/mga/sps/authsvc?StateId=oT1rTEe4rxxmjGJhCmdBR8BIG5sjHp6xrsl9ACC4fQDOvmCNwes7bojeTOks1bxuTpDKaEpAud0hGaKVTHCt4q8itCuGfRnBkLPNSgxxgu0VL378TYrJRhPWXCxsMIh8">

	<div class="container">
	  <div class="row" id="pwd-container">
	    <div class="col-md-4"></div>

	    <div class="col-md-4">
	      <section class="login-form">
	          <div class="logoimage"><img src="/mga/sps/static/logo.png" class="img-responsive center-block" alt="LOGO"></div>
            <input type="text" name="username" placeholder="User ID or E-mail" required="" class="form-control input-lg" value="">

	          <input type="password" name="password" class="form-control input-lg" id="password" placeholder="Password" required="">
	          <button type="submit" name="operation" value="verify" class="btn btn-lg btn-primary btn-block">Sign in</button>
	          <div>
	         <a href="https://husqvarna.service-now.com/pwd?id=pwd_reset_page">Reset Password</a>
	          </div>
	      </section>
	      </div>
	      <div class="navbar navbar-fixed-bottom">
	      	<div class="container">Copyright © Husqvarna AB (publ). All rights reserved.</div>
	      	</div>
	   </div>

	</div>
	    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
	    <script src="/mga/sps/static/jquery.min.js"></script>
		<!-- Latest compiled and minified JavaScript -->
		<script src="/mga/sps/static/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous">
		</script>
<input type="HIDDEN" name="login-form-type" value="pwd">
</form>
    '''

    def parse(self,response):
        csrf_token = response.xpath('//*[@name="csrf_token"]/@value').extract_first()

        print(csrf_token)
        yield FormRequest.from_response(response, formdata={'csrf_token': csrf_token, 'username':'D1037749', 'password': 'iU521hDE'}, callback=self.parse_after_login)

    def parse_after_login(self,response):
        print(response.xpath('.//div[@class = "col-md-4"]/p/a/text()'))
