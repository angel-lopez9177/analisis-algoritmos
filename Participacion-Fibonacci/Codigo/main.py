#from memory_profiler import profile
import time
import matplotlib.pyplot as plt
import multiprocessing as mp

STEP = 1
MIN = 1
MAX = 15 + STEP

@profile
def FibonacciNP(n):
    if n<= 0:
        print("Incorrect input")
    # First Fibonacci number is 0
    elif n == 1:
        return 0
    # Second Fibonacci number is 1
    elif n == 2:
        return 1
    else:
        return FibonacciNP(n-1)+FibonacciNP(n-2)

@profile
def fibonacciDP(n):
    """Necesita de la variable global FibArray"""
    if not globals().get('FibArray'):
        return Exception("La variable global FibArray no está definida")
    global FibArray
    if n<0:
        print("Incorrect input")
    elif n<= len(FibArray):
        return FibArray[n-1]
    else:
        temp_fib = fibonacciDP(n-1)+fibonacciDP(n-2)
        FibArray.append(temp_fib)
        return temp_fib

def run_fibonacci_np(min_n, max_n, step, result_queue):
    """Ejecuta FibonacciNP y pone los resultados en una cola."""
    print("Iniciando proceso para FibonacciNP...")
    timesNP = []
    secuencia = []
    for n in range(min_n, max_n, step):
        tic = time.time()
        secuencia.append(FibonacciNP(n))
        toc = time.time()
        timesNP.append(toc-tic)
    result_queue.put({'secuencia': secuencia, 'times': timesNP})
    print("Proceso para FibonacciNP terminado.")

def run_fibonacci_dp(min_n, max_n, step, result_queue):
    """Ejecuta fibonacciDP y pone los resultados en una cola."""
    print("Iniciando proceso para FibonacciDP...")
    timesDP = []
    for n in range(min_n, max_n, step):
        global FibArray
        FibArray = [0, 1] 
        tic = time.time()
        fibonacciDP(n)
        toc = time.time()
        timesDP.append(toc-tic)
    result_queue.put({'times': timesDP})
    print("Proceso para FibonacciDP terminado.")
    
if __name__ == "__main__":

    FibArray = [0, 1] 
    
    q = mp.Queue()
    p_np = mp.Process(target=run_fibonacci_np, args=(MIN, MAX, STEP, q))
    p_dp = mp.Process(target=run_fibonacci_dp, args=(MIN, MAX, STEP, q))
    p_np.start()
    p_dp.start()
    p_np.join()
    p_dp.join()
    """print("\nAmbos procesos han finalizado. Recolectando resultados...")
    results1 = q.get()
    results2 = q.get()
    
    if 'secuencia' in results1:
        data_np = results1
        data_dp = results2
    else:
        data_np = results2
        data_dp = results1
    secuencia = data_np['secuencia']
    timesNP = data_np['times']
    timesDP = data_dp['times']

    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(range(MIN, MAX, STEP),timesNP, label='FibonacciNP')
    ax1.set_ylabel('Time (s)')
    ax1.set_xlabel('n (Fibonacci number)')
    ax1.set_title('Fibonacci NP Time Complexity')
    ax2.plot(range(MIN, MAX, STEP),timesDP, label='FibonacciDP')
    ax2.set_ylabel('Time (s)')
    ax2.set_xlabel('n (Fibonacci number)')
    ax2.set_title('Fibonacci DP Time Complexity')
    print(f"La secuencia de Fibonacci es: {secuencia}")
    fig.show()
    plt.show(block=True)"""