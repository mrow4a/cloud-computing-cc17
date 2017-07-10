#!/usr/bin/env python3
# -*- python -*-
#

import configparser
import sys
import os
import subprocess
import json, time
import numpy as np

filepath = os.path.dirname(os.path.realpath(__file__))
configfile = os.path.join(filepath, 'config')
configParser = configparser.RawConfigParser()
configFilePath = configfile
configParser.read(configFilePath)

aws_key_id = configParser.get('aws', 'awsKeyId')
aws_secret = configParser.get('aws', 'awsSecret')
pemfile = configParser.get('aws', 'pemLocation')
keyLocation = configParser.get('openstack', 'keyLocation')
op_ip = configParser.get('openstack', 'opIP')

def print_help():
    print('benchmark.py <num_of_iterations>')
    print('Example ./benchmark.py 1')
    print('** Remember about filling your config file! **')

## AWS HELP FUNCTIONS

def init_aws():
    result = subprocess.run(['aws', 'ec2', 'run-instances', '--image-id', 'ami-f52bfa9a', '--count', '1', '--instance-type', 'm3.medium', '--key-name', 'group32-key', '--security-groups', 'group32-securityGroup'], stdout=subprocess.PIPE)
    data = json.loads(result.stdout.decode('utf-8'))
    instance_id = data['Instances'][0]['InstanceId']
    print('** Initializing AWS Instance...')
    while(not is_aws_running(instance_id)):
        time.sleep(2)
    print('** AWS Instance initialized')
    return instance_id

def terminate_aws(instance_id):
    # aws ec2 terminate-instances --instance-ids i-001be48dce290e70e
    result = subprocess.run(['aws', 'ec2', 'terminate-instances', '--instance-ids', instance_id], stdout=subprocess.PIPE)
    print(result.stdout.decode('utf-8'))
    pass

def is_aws_running(instance_id):
    #aws ec2 describe-instance-status --instance-id i-02438514d865477f5
    result = subprocess.run(['aws', 'ec2', 'describe-instance-status', '--instance-ids', instance_id], stdout=subprocess.PIPE)
    data = json.loads(result.stdout.decode('utf-8'))
    if(len(data['InstanceStatuses']) > 0 and data['InstanceStatuses'][0]['InstanceState']['Code'] == 16):
        print (data['InstanceStatuses'][0])
        return True
    return False

def get_aws_ip(instance_id):
    #aws ec2 describe-instance-status --instance-id i-02438514d865477f5
    result = subprocess.run(['aws', 'ec2', 'describe-instances', '--instance-ids', instance_id], stdout=subprocess.PIPE)
    data = json.loads(result.stdout.decode('utf-8'))
    instance_ip = data['Reservations'][0]['Instances'][0]['PublicIpAddress']
    print(instance_ip)
    return instance_ip

## MEMORY BENCH

def run_mem_benchmark_local(iteration):
    print('** Running MEM Benchmark LOCAL iteration:', iteration)
    filepath = os.path.dirname(os.path.realpath(__file__))
    target = os.path.join(filepath, 'memory_benchmark', 'memsweep.sh')
    result = subprocess.run([target], stdout=subprocess.PIPE, cwd=os.path.join(filepath, 'memory_benchmark'))
    output = result.stdout.decode('utf-8')

    if "Memsweep time in seconds: " not in output:
        print(result)

    start = output.find('Memsweep time in seconds: ') + 26
    bench = float(output[start:])
    print(bench)
    return bench

def run_mem_benchmark_aws(iteration, ip):
    print('** Running MEM Benchmark AWS iteration:', iteration)
    result = subprocess.run("ssh -i %s ec2-user@%s 'cd memory_benchmark && ./memsweep.sh'"%(pemfile, ip), shell=True, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')

    if "Memsweep time in seconds: " not in output:
        print(result)

    start = output.find('Memsweep time in seconds: ') + 26
    bench = float(output[start:])
    print(bench)
    return bench

def run_mem_benchmark_openstack(iteration):
    print('** Running MEM Benchmark OPENSTACK iteration:', iteration)

    result = subprocess.run("ssh -i %s ubuntu@%s 'cd memory_benchmark && ./memsweep.sh'"%(keyLocation, op_ip), shell=True, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')

    if "Memsweep time in seconds: " not in output:
        print(result)

    start = output.find('Memsweep time in seconds: ') + 26
    bench = float(output[start:])
    print(bench)
    return bench

## CPU BENCH

def run_cpu_benchmark_local(iteration):
    print('** Running CPU Benchmark LOCAL iteration:', iteration)
    filepath = os.path.dirname(os.path.realpath(__file__))
    target = os.path.join(filepath, 'cpu_benchmark', 'linpack.sh')
    result = subprocess.run([target], stdout=subprocess.PIPE, cwd=os.path.join(filepath, 'cpu_benchmark'))
    output = result.stdout.decode('utf-8')

    if "Benchmark result:" not in output:
        print(result)

    start = output.find('Benchmark result: ') + 18
    end = output.find(' KFLOPS', start)
    bench  = float(output[start:end])
    print(bench)
    return bench


def run_cpu_benchmark_aws(iteration, ip):
    print('** Running CPU Benchmark AWS iteration:', iteration)
    result = subprocess.run("ssh -i %s ec2-user@%s 'cd cpu_benchmark && ./linpack.sh'"%(pemfile, ip), shell=True, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')

    if "Benchmark result:" not in output:
        print(result)

    start = output.find('Benchmark result: ') + 18
    end = output.find(' KFLOPS', start)
    bench  = float(output[start:end])
    print(bench)
    return bench

def run_cpu_benchmark_openstack(iteration):
    print('** Running CPU Benchmark Openstack iteration:', iteration)
    result = subprocess.run("ssh -i %s ubuntu@%s 'cd cpu_benchmark && ./linpack.sh'"%(keyLocation, op_ip), shell=True, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')

    if "Benchmark result:" not in output:
        print(result)

    start = output.find('Benchmark result: ') + 18
    end = output.find(' KFLOPS', start)
    bench  = float(output[start:end])
    print(bench)
    return bench

## DISK BENCH

def prepare_tar():
    print('** Prepare tar to be send')
    import tarfile
    tar = tarfile.open(os.path.join(filepath,"benchmark.tar.gz"), "w:gz")
    for name in ["cpu_benchmark", "memory_benchmark", "disk_benchmark"]:
        tar.add(name)
    tar.close()

def send_tar_aws(ip):
    print('** Initialize connection with AWS, install scp and send tar')
    time.sleep(25)
    tarfile = os.path.join(filepath,"benchmark.tar.gz")
    subprocess.call("ssh -i %s ec2-user@%s 'sudo yum install -y openssh-clients'"%(pemfile, ip), shell=True)
    subprocess.call("scp -i %s %s ec2-user@%s:/home/ec2-user/"%(pemfile, tarfile, ip), shell=True)

    print('** Unpack tar')
    subprocess.call("ssh -i %s ec2-user@%s 'tar -zxvf benchmark.tar.gz'"%(pemfile, ip), shell=True)

def send_tar_openstack():
    print('** Initialize connection with OpenStack and send tar')
    tarfile = os.path.join(filepath,"benchmark.tar.gz")
    subprocess.call("scp -i %s %s ubuntu@%s:/home/ubuntu/"%(keyLocation, tarfile, op_ip), shell=True)

    print('** Unpack tar')
    subprocess.call("ssh -i %s ubuntu@%s 'tar -zxvf benchmark.tar.gz'"%(keyLocation, op_ip), shell=True)

def main(argv):
    print('** Remember to execute all prerequisites from awsinfo.txt before running this script!! **')
    if len(argv) != 1:
        print_help()
        sys.exit(2)

    num_iterations = int(argv[0])

    # Initialize AWS
    instance_id = init_aws()

    # Get AWS IP
    ip = get_aws_ip(instance_id)

    # Prepare TAR with scripts
    prepare_tar()
    send_tar_aws(ip)
    send_tar_openstack()

    cpu_results_local = []
    cpu_results_aws = []
    cpu_results_openstack = []
    mem_results_local = []
    mem_results_aws = []
    mem_results_openstack = []
    disk_results_local = []
    disk_results_aws = []
    disk_results_openstack = []
    random_write_disk_results_local = []
    random_write_disk_results_aws = []
    random_write_disk_results_openstack = []
    for i in range (0, num_iterations):
        cpu_results_local.append(run_cpu_benchmark_local(i+1))
        cpu_results_openstack.append(run_cpu_benchmark_openstack(i+1))
        cpu_results_aws.append(run_cpu_benchmark_aws(i+1, ip))
        mem_results_local.append(run_mem_benchmark_local(i+1))
        mem_results_openstack.append(run_mem_benchmark_openstack(i+1))
        mem_results_aws.append(run_mem_benchmark_aws(i+1, ip))

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1)
    local_mem, = ax.plot(mem_results_local, 'b^', label="Local avg %ss"%(np.average(mem_results_local)))
    aws_mem, = ax.plot(mem_results_aws, 'g^', label="AWS avg %ss"%(np.average(mem_results_aws)))
    ops_mem, = ax.plot(mem_results_openstack, 'r^', label="OpenStack avg %ss"%(np.average(mem_results_openstack)))
    plt.legend(handles=[local_mem, aws_mem, ops_mem])
    plt.ylabel('Memsweep (s)')
    plt.xlabel('Iterations')
    plt.xlim([-1, num_iterations])
    ax.set_xticklabels([])

    fig, ax = plt.subplots(1)
    local_cpu, = ax.plot(cpu_results_local, 'b^', label="Local avg %s"%(np.average(cpu_results_local)))
    aws_cpu, = ax.plot(cpu_results_aws, 'g^', label="AWS avg %s"%(np.average(cpu_results_aws)))
    ops_cpu, = ax.plot(cpu_results_openstack, 'r^', label="OpenStack avg %s"%(np.average(cpu_results_openstack)))
    plt.legend(handles=[local_cpu, aws_cpu, ops_cpu])
    plt.ylabel('KiloFlops')
    plt.xlabel('Iterations')
    plt.xlim([-1, num_iterations])
    ax.set_xticklabels([])

    plt.show()

    #Terminate AWS after all
    terminate_aws(instance_id)
if __name__ == '__main__':
    main(sys.argv[1:])
