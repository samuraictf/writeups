# Dubkey

This problem tasks us with signing a given message, given the ability to sign up to 255 other messages.

The signature algorithm acts on a 128-byte `M`, and has a 128-byte secret, `S`. First, `S` is prepended to `M`, giving us `T = S | M`, a 256-byte string.

Next, a directed graph is constructed as follows:

1) For i in [0, 255], construct a vertex `V_i`

2) For i in [0, 255], construct an edge from `V_i` to `V_(ord(T[i]))`

The signature is then computed as the product of the lengths of the longest paths beginning at each vertex.

We first make the observation that if we choose `M = chr(128) | chr(129) | ... | chr(255)`, then all of the paths from vertices [128, 255] will have length 1, and won't contribute to the signature.

We can use this fact to determine what vertices are reachable from the vertices associated with the secret. Consider `M` with `M[0]` set to `chr(255)`. If `V_128` is not referenced in the secret, then none of the path lengths will change, and the signature will remain the same. However, if `V_128` is reachable, then one of the paths will have longer length, and the signature will increase.

We use this process to find two root nodes, `r_1` and `r_2` for the directed graph of the signature we're trying to forge. We can then simply swap these two nodes to produce a second message that results in the required signature.

We use the oracle to determine the signature of this message, then submit it, resulting in the flag: `9447{Th1s_ta5k_WAs_a_B1T_0F_A_DaG}`
