# Fibbed

This problem involves decrypting a flag that was encrypted using a Diffie Hellman scheme. The key consists of the pair `(r, e)`. Here, `r` is public matrix in `Z_p`, and `e` is a secret, random element of `Z_p`.

The pcap gives us the following:

```
p: 981725946171163877
server_r (one row of it): [58449491987662952, 704965025359609904]
client_r (one row of it): [453665378628814896, 152333692332446539]
ciphertext: 59719af4dbb78be07d0398711c0607916dd59bfa57b297cd220b9d2d7d217f278db6adca88c9802098ba704a18cce7dd0124f8ce492b39b64ced0843862ac2a6
```

The matrix is calculated using the following function:

```python
def calcM(p, l, base):
	if l == 0:
		return [[base[1], base[0]], [base[0], base[1]]]
	x1 = [[base[0], base[1]], [base[1], (base[0] + base[1]) % p]]
	x2 = mult(x1, x1, p)
	for i in bin(l)[3:]:
		if i == '1':
			x1 = mult(x1, x2, p)
			x2 = mult(x2, x2, p)
		else:
			x2 = mult(x1, x2, p)
			x1 = mult(x1, x1, p)
	return x1
    
  r = calcM(p, e, (0, 1))
  ```
  
Looking carefully at the implementation, it is clear that for the base `(0, 1)`, this computes `Q^e (mod p)`, where `Q` is the [Fibonacci Q-Matrix](http://mathworld.wolfram.com/FibonacciQ-Matrix.html). Since we know that [Binet's Formula](http://mathworld.wolfram.com/BinetsFibonacciNumberFormula.html) is a closed-form solution to the Fibonacci sequence, we can use its inverse to compute `e` from `r`. This gives us that `e` is `152333692332446539`, which we can use to decrypt the ciphertext: `9447{Pisan0_mU5t_nEv3r_hAve_THougHt_0f_bruTe_f0rce5}`
