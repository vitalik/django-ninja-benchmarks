import time
import re
import os
import sys
import subprocess


C1_FRAMEWORKS = [
    'flask_marshmallow_uwsgi',
    'drf_uwsgi',
    'ninja_uwsgi',
    'ninja_uvicorn',
    'ninja_uwsgi_pydantic2',
    'fastapi_uvicorn_pydantic2',
    'fastapi_uvicorn',
]

CONCURRENT_FRAMEWORKS = [
    # 'fastapi_uvicorn',
    # 'flask_marshmallow_uwsgi',
    # 'drf_uwsgi',
    'ninja_uvicorn',
    'ninja_uwsgi_pydantic2',
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
    # print(output)
    rps = re.findall(r'Requests per second: \s+(.*?)\s', output)[0]
    p50 = re.findall(r'\s+50%\s+(\d+)', output)[0]
    p99 = re.findall(r'\s+99%\s+(\d+)', output)[0]
    return (rps, p50, p99)


def preheat():
    benchmark('http://127.0.0.1:8000/api/create', 1, 5, 'payload.json')
    benchmark('http://127.0.0.1:8000/api/iojob', 1, 5)


def run_c1_test():
    return benchmark('http://127.0.0.1:8000/api/create', 1, 1000, 'payload.json')



def test_c1(name, workers_cases):
    results = {}
    for n_workers in workers_cases:
        print(f'--- {name} {n_workers} -------------------------------------------')
        with FrameworkService(name, n_workers):
            preheat()
            res = benchmark('http://127.0.0.1:8000/api/create', 1, 3000, 'payload.json')
            results[n_workers] = res
    return results

def test_concurrent(name, workers_cases):
    results = {}
    for n_workers in workers_cases:
        print(f'--- {name} {n_workers} -------------------------------------------')
        with FrameworkService(name, n_workers):
            preheat()
            res = benchmark('http://127.0.0.1:8000/api/iojob', 50, 200)
            results[n_workers] = res
    return results


def run(title, frameworks, func, workers_cases):

    results = {}
    for framework in frameworks:
        results[framework] = func(framework, workers_cases)

    print(title)
    print(f'{"Framework/Workers":<26} :', end='')
    for w in workers_cases:
        print(f'{w:>9}', end='')
    print('')
    for framework, results in sorted(results.items()):
        print(f'{framework:<26} :', end='')
        for w in workers_cases:
            print(f'{results[w][0]:>9}', end='')
        print('')


def main():
    # os.system(f'docker-compose build')
    os.system('docker build --tag=benchmark-common .')
    os.system('docker build --tag=benchmark-pydantic2 -f Dockerfile.pydantic2 .')

    os.system(f'docker-compose down')

    # run('Concurrent test', CONCURRENT_FRAMEWORKS, test_concurrent, [1,2,5,10])
    run('CPU/parsing test', C1_FRAMEWORKS, test_c1, [1])

if __name__ == '__main__':
    main()
