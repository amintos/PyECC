from Key import Key
import time
from rijndael import encrypt, decrypt
from collections import OrderedDict


from elliptic import _signed_bin, euclid, to_projective, addf, mulf, muladdf, doublef
from curves import get_curve

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

def test_signed_binary_perf(n = 100):
    results = OrderedDict()
    for bits in (192, 224, 256, 384, 521):
        p = Key.generate(bits)._priv[1]
        t = time.time()
        for i in xrange(n):
            _signed_bin(p)
        t = time.time() - t
        results[bits] = t
    return results

def test_euclid_perf(n = 100):
    results = OrderedDict()
    for bits in (192, 224, 256, 384, 521):
        p, q = Key.generate(bits)._pub[1]
        t = time.time()
        for i in xrange(n):
            euclid(p, q)
        t = time.time() - t
        results[bits] = t
    return results

def test_fast_add_perf(n = 100):
    results = OrderedDict()
    for bits in (192, 224, 256, 384, 521):
        p1 = [Key.generate(bits)._pub[1] for i in xrange(n)]
        p2 = [Key.generate(bits)._pub[1] for i in xrange(n)]
        
        jp1 = map(to_projective, p1)
        jp2 = map(to_projective, p2)

        _, modulus, _, p, q, _ = get_curve(bits)
        
        t = time.time()
        for i in xrange(n):
            addf(modulus, p, q, jp1[i], jp2[i])
        t = time.time() - t
        results[bits] = t
    return results

def test_fast_double_perf(n = 100):
    results = OrderedDict()
    for bits in (192, 224, 256, 384, 521):
        p1 = Key.generate(bits)._pub[1]   
        jp1 = to_projective(p1)
        _, modulus, _, p, q, _ = get_curve(bits)
        
        t = time.time()
        for i in xrange(n):
            doublef(modulus, p, q, jp1)
        t = time.time() - t
        results[bits] = t
    return results

def test_fast_multiply_add_perf(n = 100):
    results = OrderedDict()
    for bits in (192, 224, 256, 384, 521):
        p1 = Key.generate(bits)._pub[1]
        p2 = Key.generate(bits)._pub[1]
        
        jp1 = to_projective(p1)
        jp2 = to_projective(p2)

        c1 = p2[0]
        c2 = p1[0]
        
        _, modulus, _, p, q, _ = get_curve(bits)
        
        t = time.time()
        for i in xrange(n):
            muladdf(modulus, p, q, jp1, c1, jp2, c2)
        t = time.time() - t
        results[bits] = t
    return results

def test_slow_multiply_add_perf(n = 100):
    results = OrderedDict()
    for bits in (192, 224, 256, 384, 521):
        p1 = Key.generate(bits)._pub[1]
        p2 = Key.generate(bits)._pub[1]
        
        jp1 = to_projective(p1)
        jp2 = to_projective(p2)

        c1 = p2[0]
        c2 = p1[0]
        
        _, modulus, _, p, q, _ = get_curve(bits)
        
        t = time.time()
        for i in xrange(n):
            addf(modulus, p, q,
                     mulf(modulus, p, q, jp1, c1),
                     mulf(modulus, p, q, jp2, c2))
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
#print_dict("Fast Double", test_fast_double_perf(10000))
#print_dict("Fast Multiply-Add", test_fast_multiply_add_perf(n))
#print_dict("Slow Multiply-Add", test_slow_multiply_add_perf(n))
print_dict("Key generation", test_generation_perf(n))
print_dict("Signing", test_signing_perf(n))
print_dict("Verifying", test_verification_perf(n))


n = 1000
#print_dict("Fast Point Addition", test_fast_add_perf(n))
#print_dict("Euclidean Algorithm", test_euclid_perf(n))
#print_dict("Signed Binary Expansion", test_signed_binary_perf(n))
print_dict("AES Encryption", test_cryption(n, encrypt))
print_dict("AES Decryption", test_cryption(n, decrypt))


