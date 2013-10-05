Hokay! MP1 Harsh Singh (hsingh23) + Ziqi Peng ()

Setup:
chmod +x times.py server.py client.py generate_bytes.sh

Server:
./server -p 9000

Client:
./client.py -p 9000 -d localhost -f 100b

Files:
1000000b, 100000b, 10000b, 1000b, 100b, 1b

Benchmark:
See benchmark file or
./times.py

Generate new random files:
./generate_bytes.sh