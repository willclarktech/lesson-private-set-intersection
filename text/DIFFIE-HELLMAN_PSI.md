# Private set intersection based on Diffie-Hellman key exchange

In this section we will outline a private set intersection (PSI) protocol based on the Diffie-Hellman key exchange. It might be helpful to revisit the Cryptography lesson to refresh your memory on Diffie-Hellman key exchange as well as primitive roots and prime number generation.

## The protocol

The basic idea is that Alice and Bob will use the Diffie-Hellman technique to derive a unique key for each element in each of their sets. The intersection consists of those values from which matching keys are derived.

Here’s how the protocol works:

1. Alice and Bob agree on a large prime $$p$$.
1. Alice randomly generates a private key $$a$$.
1. Alice repeatedly hashes each of the values in her original set until they are all primitive roots modulo $$p$$. (See below.)
1. For each of these hashed values, Alice calculates $$g^a \mod p$$ where $$g$$ is the hashed value.
1. Alice sends $$p$$ and her calculated values to Bob.
1. Bob randomly generates a private key $$b$$.
1. Bob repeatedly hashes each of the values in his original set until they are all primitive roots modulo $$p$$.
1. For each of these hashed values, Bob calculates $$g^b \mod p$$ where $$g$$ is the hashed value.
1. Bob calculates shared keys corresponding to each element in Alice’s original set by raising the values received from Alice to the power of his private key, i.e. $$g^{ab} \mod p$$ for each hashed value $$g$$.
1. Bob sends his calculated values ($$g^b \mod p$$) to Alice, as well as the calculated shared keys corresponding to the elements in Alice’s original set.
1. Alice calculates the shared keys corresponding to each element in Bob’s original set by raising the values received from Bob to the power of her private key, i.e. $$g^{ba} = g^{ab} \mod p$$ for each of Bob’s hashed values, $$g$$.
1. Alice compares the shared keys calculated from the elements in her own original set with the shared keys calculated using Bob’s elements. The intersection consists of those elements in Alice’s original set whose shared key can also be found in the set of shared keys calculated from the elements in Bob’s original set.

Note that the hashing in steps 3 and 7 is necessary because the Diffie-Hellman protocol requires the base value $$g$$ to be a primitive root modulo $$p$$.

In the end Bob only sees the values Alice hashed and obscured using her private key ($$g^a \mod p$$), while Alice only sees the similarly obscured values from Bob’s set, as well as her own obscured values raised to the power of Bob’s private key ($$g^{ab} \mod p$$). Of course Eve the eavesdropper also sees these values. When using Diffie-Hellman for key exchange, these shared keys are sensitive, but in our PSI protocol they are also visible to Eve. That’s fine though, because they aren’t then used for encryption, just comparison. The important thing is that without Alice’s private key (or Bob’s), Eve cannot reconstruct either of their sets (the sensitive data in this situation) or find out anything about their intersection (because she only sees one set of shared keys).

## Extending the protocol

As with the PSI protocol based on the Paillier cryptosystem which we saw in the previous section, this protocol can be extended to reveal only the intersection _size_ to the client. In order to determine the intersection, it is important that Bob returns the shared keys corresponding to Alice’s values in the same order he receives them, so that Alice knows which elements in her set are the corresponding ones. However, if Bob shuffles those shared keys before returning them to Alice, Alice will not be able to connect the shared keys back to specific elements, though she will still be able to see how many elements are common to the two sets. One simple way for Bob to do this would be for him to sort the shared keys numerically, since without his secret key the values should appear uniform.

It’s not possible (as far as I’m aware!) to develop this into a protocol which just gives Alice a boolean answer “intersection is empty” or “intersection is not empty”, as we were able to with the Paillier-based PSI protocol.

## Pros and cons of PSI based on Diffie-Hellman

When we looked at PSI based on the Paillier cryptosystem, we saw there were several limitations. Some of those limitations also apply to this Diffie-Hellman PSI protocol, including the assumption that the server and client are honest, and even with the size-only protocol a malicious client could derive the full server set if the domain is small enough.

An additional weakness is that the size of each party’s set is leaked to the other party (and any eavesdroppers), because only values relating to each element are sent to the other party. However, the flipside of this is that this protocol is much more practical for large domains because we do not need to perform calculations on values not in either set, and do not need to transfer them across a connection either.

Another limitation is that steps 3 and 7 of the protocol involve a computationally intensive calculation: hashing numbers until they are primitive roots. Your implementation is likely to be very slow, even if you spend time optimizing these steps to be more efficient. We will revisit this issue after the implementation challenge.

### Quiz

1. Which of the following variants are possible with a PSI protocol based on Diffie-Hellman?
    - reveal the intersection (correct)
    - reveal only the size of the intersection (correct)
    - reveal only whether or not the intersection is empty
