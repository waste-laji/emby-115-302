### 功能

获取alist直链，搭配emby使用
alist添加存储需启用签名


### 安装依赖&nginx配置

pip install requests
pip install flask
pip install flask_cors


在location中添加
if ($request_uri ~* /videos/\d*/stream)
{
    proxy_pass http://127.0.0.1:60000;
}

if ($request_uri ~* /emby/videos/\d+/original\.*)
{
    proxy_pass http://127.0.0.1:60000;
}

if ($request_uri ~* /videos/\d+/.*)
{
    proxy_pass http://127.0.0.1:60000;
}



例:

server
{
	
	#PROXY-START/
	listen 9999;
	server_name 127.0.0.1;
	

	
	location ^~ /
	{
        #emby的url
	    proxy_pass http://127.0.0.1:8096;
	    
    
	   if ($request_uri ~* /videos/\d*/stream)
	    {
	      proxy_pass http://127.0.0.1:60000;
	    }

	   if ($request_uri ~* /emby/videos/\d+/original\.*)
	    {
	      proxy_pass http://127.0.0.1:60000;
	    }

	   if ($request_uri ~* /videos/\d+/.*)
	    {
	      proxy_pass http://127.0.0.1:60000;
	    }


	   client_max_body_size 5000M;
	   proxy_set_header X-Real-IP $remote_addr;
	   proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	   proxy_set_header X-Forwarded-Proto $scheme;
	   proxy_set_header Sec-WebSocket-Extensions $http_sec_websocket_extensions;
	   proxy_set_header Sec-WebSocket-Key $http_sec_websocket_key;
	   proxy_set_header Sec-WebSocket-Version $http_sec_websocket_version;
       proxy_set_header Upgrade $http_upgrade;
	   proxy_set_header Connection "upgrade";

	   proxy_cache off;
	   proxy_redirect off;
	   proxy_buffering off;

       add_header 'Access-Control-Allow-Origin' '*';
       add_header 'Access-Control-Allow-Credentials' 'true';
       add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
       add_header 'Access-Control-Allow-Headers' 'Origin, Content-Type, Accept, Authorization, X-Requested-With';
        
	   proxy_ssl_verify off;
	   proxy_http_version 1.1;
	   proxy_read_timeout 120;
	
	
	}

}