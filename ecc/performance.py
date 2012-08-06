from Key import Key
import time
from rijndael import encrypt, decrypt
from collections import OrderedDict

def test_generation_perf(n = 100):
    results = OrderedDict()
    for bits in (192, 224, 256, 384, 521):
        t = time.time()
        for i in xrange(n):
            k = Key.generate(bits)
        t = time.time() - t
        results[bits] = t
    return results
        
def test_signing_perf(n = 100):
    results = OrderedDict()
    for bits in (192, 224, 256, 384, 521):
        k = Key.generate(bits)
        t = time.time()
        for i in xrange(n):
            k.sign("random string")
        t = time.time() - t
        results[bits] = t
    return results

def test_verification_perf(n = 100):
    results = OrderedDict()
    for bits in (192, 224, 256, 384, 521):
        k = Key.generate(bits)
        s = k.sign("random string")
        t = time.time()
        for i in xrange(n):
            k.verify("random string", s)
        t = time.time() - t
        results[bits] = t
    return results

def test_cryption(n, method):
    results = OrderedDict()
    for ks in (16, 24, 32):
        for bs in (16, 24, 32):
            k = 'x' * ks
            b = 'y' * bs
            t = time.time()
            for i in xrange(n):
                method(k, b)
            results['Keysize %s / Blocksize %s' % (ks * 8,
                                                   bs * 8)] = time.time() - t
    return results

            
def print_dict(title, d):
    print title
    print '-' * len(title)
    for k, v in d.items():
        print k, '\t', v
    print

n = 100
#print_dict("Key generation", test_generation_perf(n))
#print_dict("Signing", test_signing_perf(n))
#print_dict("Verifying", test_verification_perf(n))

n = 1000
print_dict("AES Encryption", test_cryption(n, encrypt))
print_dict("AES Decryption", test_cryption(n, decrypt))

        
