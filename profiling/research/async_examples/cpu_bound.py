
from concurrent.futures import ThreadPoolExecutor, as_completed

a = '''this is a this is bytes bytes file file file to test bigram bigram counting.
for what it's worth worth here is some more tasty data.'''.split( )





def skipgramAsync( idx ):
    try:
        return (a[idx], a[idx+2])
    except IndexError as e:
        print(e)
    

if __name__ == "__main__":
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [ ] 
        for k,v in enumerate(a):
            futures.append(executor.submit( skipgramAsync, k ))
        for future in as_completed(futures):
            print(future.result( ))
