#!/usr/bin/env python2.7

import web
import hashlib
import os, sys
import errno

#sys.path.append(os.path.dirname(__file__))

web.config.debug = True

urls = (
    '/', 'index',
    '/stor', 'stor',
)

namespace = "data"

class index:
    def GET(self):
        return "Hello, world"

class stor:
    def GET(self):
        return """<html><head></head><body>
<form method="POST" enctype="multipart/form-data" action="">
<input type="text" name="folder" /><br/>
<input type="file" name="fileinfo" />
<br/>
<input type="submit" />
</form>
</body></html>"""

    def POST(self):
        try:
            data      = web.input(fileinfo={})

            filename  = data['fileinfo'].filename
            folder    = data['folder']

            if len(filename) == 0:
                raise AttributeError("missing filename")

            m = hashlib.md5()
            if len(folder) > 1:
                m.update(folder)
                folder = '/'+ folder
            else:
                m.update(filename)

            h = m.hexdigest()
            path = "%s/%s/%s/%s%s" % (namespace, h[0:1], h[1:3], h[3:4], folder)
   
            try: 
                os.makedirs(path)
            except OSError, e:
                if e.errno == errno.EEXIST:
                    pass

            f = open("%s/%s" % (path, filename), "w")
            f.write(data['fileinfo'].file.read())
            f.close()

            return "%s/%s" % (path, filename)

        except AttributeError, e:
            return 'AttributeError', str(e)

        except Exception, e:
            return 'Exception', str(e)

#app = web.application(urls, globals())
#app.run()  '''      
app = web.application(urls, globals())
application = app.wsgifunc()
