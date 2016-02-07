#!/usr/bin/env ruby

require 'json'

def create_partial_json_log()
  dump=`git log \
    --pretty=format:'{%n  "commit": "%H",%n  "author": "%an <%ae>",%n  "date": "%ad",%n  "message": "%f"%n},'`
  dump="[" + dump[0,dump.length-1] + "]"
  print dump
  Json.parse(dump)
end

log =`git --no-pager log --name-status --format='%H'`

commited_files=`git --no-pager log --name-only --format='%H' --pretty=format:''`.split(/\n\n/)

print create_partial_json_log()
puts





puts log_formatted_json

c = []
for files_per_revision in commited_files
  print files_per_revision.split(/\n/)
  puts
  c << files_per_revision.split(/\n/)
end

def split_dumped_log_by_commit(log)
  commits=[]
  _commit={}
  for line in log
  end
end
