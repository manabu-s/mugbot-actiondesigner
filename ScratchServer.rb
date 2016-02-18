#! /usr/bin/ruby
# coding: utf-8

require 'rubygems'
require 'serialport'
require 'socket'
require 'json'

port =  "/dev/ttyACM0"
sp = SerialPort.new(port, 9600, 8, 1, SerialPort::NONE)

server = TCPServer.open(51234)

print("Start Mugbot Scratch Server...\n")

while true
  Thread.start(server.accept) do | sock |
    system(`jsay スクラッチとの接続を開始しました`)
    while buf = sock.gets
      begin
        json = JSON.parse(buf)
        sock.write(buf)
        case json['action']
        when 'face_y' then
          y = json['arg'].to_i + 95
          if y > 110 then
            y = 110
          elsif y < 80 then
            y = 80
          end
          sp.write(y.to_s + "y")
          sleep(0.01)
        when 'face_x' then
          x = json['arg'].to_i + 90
          if x > 175 then
            x = 175
          elsif x < 5 then
            x = 5 
          end
          sp.write(x.to_s + "x")
          sleep(0.01)
        when 'eye' then
          z = json['arg'].to_i;
          if z > 255 then
            z = 255
          elsif x < 0 then
            x = 0
          end
          sp.write(z.to_s + "z")
          sleep(0.01)
        when 'speech' then
          sp.putc "t"
          system(`jsay #{json['arg'].to_s}`)
          sp.putc "k"
        else
          print("Error\n")
        end
      rescue Exception => e
        $stderr.puts e
      end
    end
    sock.close
  end
end

server.close
