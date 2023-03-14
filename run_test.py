import os
import re
import subprocess
import time

CONCURRENT_FRAMEWORKS = [
    'flask_marshmallow_uwsgi',
    'drf_uwsgi',
    'ninja_uwsgi',
    'ninja_gunicorn',
    'ninja_uvicorn',
    'fastapi_gunicorn',
    'fastapi_uvicorn'
]


class FrameworkService:
    def __init__(self, name, workers=1):
        self.name = name
        self.workers = workers

    def __enter__(self):
        os.system(f'WORKERS={self.workers} docker-compose up -d network_service')
        os.system(f'WORKERS={self.workers} docker-compose up -d {self.name}')
        time.sleep(5)

    def __exit__(self, *a, **kw):
        os.system(f'WORKERS={self.workers} docker-compose down')


def benchmark(url, concurency, count, payload=None):
    cmd = ['ab', '-c', f'{concurency}', '-n', f'{count}']
    if payload:
        cmd += ['-l', '-p', payload, '-T', 'application/json']
    cmd += [url]
    print('> ', ' '.join(cmd))
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    assert result.returncode == 0, output
    return parse_benchmark(output)


def parse_benchmark(output: str):
    rps = re.findall(r'Requests per second: \s+(.*?)\s', output)[0]
    p50 = re.findall(r'\s+50%\s+(\d+)', output)[0]
    p99 = re.findall(r'\s+99%\s+(\d+)', output)[0]
    return rps, p50, p99


def preheat():
    benchmark('http://127.0.0.1:8000/api/create', 1, 5, 'payload.json')
    benchmark('http://127.0.0.1:8000/api/iojob', 1, 5)


WORKERS_CASES = [1, 2, 4, 8, 16, 32, 64]


def test_concurrent(name):
    results = {}
    for workers in WORKERS_CASES:
        with FrameworkService(name, workers):
            preheat()
            res = benchmark('http://127.0.0.1:8000/api/iojob', 50, 200)
            results[workers] = res
    return results


def main():
    os.system(f'docker-compose build')
    os.system(f'docker-compose down')

    results = {}
    for framework in CONCURRENT_FRAMEWORKS:
        results[framework] = test_concurrent(framework)

    print('Framework               :', end='')
    for w in WORKERS_CASES:
        print(f'{w:>9}', end='')

    print()

    for framework, results in sorted(results.items()):
        print(f'{framework:<23} :', end='')
        for w in WORKERS_CASES:
            print(f'{results[w][0]:>9}', end='')
        print()

    print('Columns indicate the number of workers in each run')
    print('Values are in requests per second - higher is better.')

if __name__ == '__main__':
    main()
