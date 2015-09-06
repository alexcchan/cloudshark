
import httplib2
import io
import json
import os
import urllib


class CloudsharkError(Exception):

    def __init__(self, msg, error_code=None):
        self.msg = msg
        self.error_code = error_code

    def __str__(self):
        return repr('%s: %s' % (self.error_code, self.msg))


class Cloudshark(object):

    def __init__(self,url,token):
        self.url = url
        self.token = token

    def get_info(self,id):
        """Get the info about a particular capture by id."""
        url = '%s/api/v1/%s/info/%s' % (self.url,self.token,id)
        http = httplib2.Http()
        (response,content) = http.request(url,method='GET')
        http_status = response.get('status')
        if http_status != '200':
            print(response)
            raise CloudsharkError('Error retrieving: %s'%url,http_status)
        return json.loads(content)

    def search_by_file_name(self,file_name):
        """Search for a capture by file name."""
        url = '%s/api/v1/%s/search?search[filename]=%s' % (self.url,self.token,urllib.quote(file_name))
        http = httplib2.Http()
        (response,content) = http.request(url,method='GET')
        http_status = response.get('status')
        if http_status != '200':
            print(response)
            raise CloudsharkError('Error retrieving: %s'%url,http_status)
        return json.loads(content)

    def upload(self,file_object,file_name=None):
        """Upload a capture file to Cloudshark."""
        url = '%s/api/v1/%s/upload' % (self.url,self.token)
        BOUNDARY = "LANDSHARKCLOUDSHARK"
        headers = {}
        headers['Content-Type'] = 'multipart/form-data; boundary=%s' % BOUNDARY
        if file_name is None:
            file_name = os.path.basename(file_object.name)
        file_content = file_object.read()
        body_lines = ['--' + BOUNDARY,
                'Content-Disposition: form-data; name="file"; filename="%s"' % file_name,
                'Content-Type: application/octet-stream',
                '',
                file_content,
                '--' + BOUNDARY + '--',
                '']
        b = io.BytesIO()
        for body_line in body_lines:
            if isinstance(body_line,unicode):
                b.write(body_line.encode('utf-8'))
            else:
                b.write(body_line)
            b.write(b'\r\n')
        body = b.getvalue()
        http = httplib2.Http()
        (response,content) = http.request(url,method='POST',body=body,headers=headers)
        http_status = response.get('status')
        if http_status != '200':
            print(response)
            raise CloudsharkError('Error retrieving: %s'%url,http_status)
        # content is a dict with "id" and "filename" entries.
        return json.loads(content)
