require 'sinatra'

get "/" do
  mpc_output = IO.popen("mpc").readlines.join("<br/>")
  "<html><body>" + 
  "  <h3>#{mpc_output}</h3>" +
  '  <p><a href="prev">prev</a> <a href="/toggle">play/pause</a> <a href="/next">next</a></p>' +
  "</body></html>"
end

get '/prev' do
  system "mpc prev"
  redirect "/"
end

get '/next' do
  system "mpc next"
  redirect "/"
end

get '/toggle' do
  system 'mpc toggle'
  redirect "/"
end
