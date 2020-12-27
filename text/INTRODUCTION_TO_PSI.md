# Introduction to private set intersection

## Which kind of problem does private set intersection solve?

Suppose Alice has a set of contacts and so does Bob. They want to find out if they have any friends in common, but since they never met before, neither of them wants to just hand over their friends’ data (names, email addresses, etc) to the other person. How can they work out whether they have any mutual contacts while respecting data privacy?

Private set intersection (PSI) refers to a set of techniques designed to solve exactly this sort of problem. And there are many other problems which have the same form. For example, how can two hospitals collaborate on a medical study by pooling data on patients who have visited both hospitals, without sacrificing the privacy of patients who have not? How can a public health authority let members of the public know they’ve been in contact with somebody who has tested positive for Covid-19 without potentially leaking information about that person’s location history?

Does it sound too good to be true? Well, any PSI protocol is going to involve some computational overhead, so it’s not entirely for free. However, in many cases the trade-off may well be worthwhile.

## A simple PSI protocol based on Homomorphic Encryption

Let’s get an intuition for how PSI is possible. If we’re working with small domains, we can build a PSI protocol on top of a homomorphic encryption scheme, such as the Paillier cryptosystem encountered in the Homomorphic Encryption lesson.

Suppose Alice (the client) and Bob (the server) each has a set of elements from some domain and Alice wants to discover the intersection of her set with Bob’s set, but Alice doesn’t want to reveal her set to Bob and Bob doesn’t want to reveal what’s in his set to Alice, besides the intersection. Here’s how the protocol could work:

1. Alice generates a public-private key pair according to the Paillier cryptosystem.
1. For each element in the domain, Alice encrypts a 1 or a 0 indicating whether that element is present in her set.
1. Alice sends the encrypted values and her public key to Bob.
1. Bob multiplies each encrypted value by a plaintext 1 or 0 depending on whether that element is present in his set, according to the Paillier multiplication process.
1. Bob sends the encrypted multiplication results back to Alice.
1. Alice decrypts the encrypted results to reveal the results of multiplying her 1s and 0s by Bob’s 1s and 0s in plaintext. The intersection consists of the elements in the domain where the multiplication result is 1.

(Multiplying these 1s and 0s is essentially the same as treating them as boolean values and performing an AND operation on them.)

Note that it is very important Bob uses a Paillier implementation which avoids the gotchas listed in the Homomorphic Encryption lesson to do with multiplying by 0 and 1. Otherwise, whenever Bob multiplies one of Alice’s encrypted values by 0, Alice or an eavesdropper will be able to detect that and infer that the corresponding elements are not in Bob’s set, that all of the other elements are in Bob’s set, and thus the protocol is not private at all. A similar problem arises if multiplication by 1 is not performed securely.

## Pros and cons of PSI based on homomorphic encryption

If followed honestly by Alice and Bob, the above protocol is pretty secure. In particular, assuming that a large enough modulus has been chosen and that the implementation is secure, any eavesdropper listening in on their communication should not be able to learn anything about Alice and Bob’s sets.

However, a malicious client could quite easily extract Bob’s complete set by sending the right kind of request. For example, Alice could send a request indicating that every element was present in her set and directly infer Bob’s set from the response. Since Alice’s information would be encrypted, Bob would not even be able to detect that Alice was performing this attack.

Another limitation of this approach is the requirement that every element in the domain needs to be encrypted, transferred from the client to the server, operated on, and transferred back to the client. These requirements scale linearly with the domain size, and are simply impractical for many use cases in terms of computational overhead as well as bandwidth.

In the next section we will take a detailed look at a PSI protocol based on Diffie-Hellman key exchange which is more efficient and offers better defences against malicious clients. Then we will implement this Diffie-Hellman PSI protocol.
