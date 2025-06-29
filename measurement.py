import zmq
import json
import time
import threading
import os
import pandas as pd

# Benchmark configuration
sizes = [100, 1000, 10000, 100000]
num_msgs = 100  # Number of round-trip messages per size

# Transport addresses
transports = {
    'inproc': 'inproc://benchmark',
    'ipc': 'ipc:///tmp/zmq_bench.sock',
    'tcp': 'tcp://127.0.0.1:5555'
}

results = []

def run_benchmark(name, addr):
    # Clean up old socket file if using IPC
    if name == 'ipc' and os.path.exists('/tmp/zmq_bench.sock'):
        os.remove('/tmp/zmq_bench.sock')

    ctx = zmq.Context()

    # Server thread: binds REP socket and echoes messages
    def server():
        sock = ctx.socket(zmq.REP)
        sock.bind(addr)
        total_msgs = len(sizes) * (num_msgs + 1)  # include warmup
        for _ in range(total_msgs):
            msg = sock.recv()
            sock.send(msg)
        sock.close()

    srv = threading.Thread(target=server, daemon=True)
    srv.start()
    time.sleep(0.1)  # allow bind

    # Client: connects REQ socket
    sock = ctx.socket(zmq.REQ)
    sock.connect(addr)

    for size in sizes:
        payload = json.dumps(list(range(size))).encode('utf-8')

        # Warmup
        sock.send(payload)
        sock.recv()

        # Measure round-trip times
        latencies = []
        for _ in range(num_msgs):
            start = time.time()
            sock.send(payload)
            sock.recv()
            end = time.time()
            latencies.append(end - start)

        avg_ms = (sum(latencies) / len(latencies)) * 1000
        results.append({
            'transport': name,
            'payload_size': size,
            'avg_latency_ms': round(avg_ms, 3)
        })

    sock.close()
    ctx.term()
    srv.join()

# Run benchmarks for each transport
for transport_name, address in transports.items():
    run_benchmark(transport_name, address)

# Display results as a dataframe
df = pd.DataFrame(results)
print(df)
