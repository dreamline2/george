import tempfile
import webapp2
import urlparse
import sys
    
def app(env, start_response):
    status = '200 OK'
    start_response(status, [])
    
    if env['REQUEST_METHOD'] != 'POST':
        template = '''
         <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
         <script>
            function exec(){
                $("#out").val("");
                data = $('[name=code]').val();
                $.ajax({
                    url:"",
                    type: "POST",
                    data: {"code": data},
                    dataType:'text'
                }).done(function(msg){
                    $('#out').val(msg)
                })
            }
         </script>
        <textarea name="code" rows=20 cols=100>
        </textarea><br/>
        <input type="submit" onclick="exec()" readonly><br/>
        <textarea id="out" rows=20 cols=100>
        </textarea>
        '''
        return [template]
    else:
        query = env['wsgi.input'].read()
        params = urlparse.parse_qs(query)
        code = params.get('code')[0]

        out = tempfile.TemporaryFile()
        sys.stdout = out
        exec(code)
        out.seek(0)
        result = out.read()
        return [result]
