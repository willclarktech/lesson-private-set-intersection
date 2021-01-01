# Introduction to private set intersection

## Which kind of problem does private set intersection solve?

Suppose Alice has a set of contacts and so does Bob. They want to find out if they have any friends in common, but since they never met before, neither of them wants to just hand over their friends’ data (names, email addresses, etc) to the other person. How can they work out whether they have any mutual contacts while respecting data privacy?

Private set intersection (PSI) refers to a set of techniques designed to solve exactly this sort of problem. And there are many other problems which have the same form. For example, how can two hospitals collaborate on a medical study by pooling data on patients who have visited both hospitals, without sacrificing the privacy of patients who have not? How can a public health authority let members of the public know they’ve been in contact with somebody who has tested positive for Covid-19 without potentially leaking information about that person’s location history?

Does it sound too good to be true? Well, any PSI protocol is going to involve some computational overhead, so it’s not entirely for free. However, in many cases the trade-off may well be worthwhile.

## A PSI protocol based on Homomorphic Encryption

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

Furthermore, two variants can be developed for slightly different use cases. The first lets the server reveal not the full intersection, but just its size. After performing the homomorphic multiplication, the server then sums all of the values together using homomorphic addition. The result, when decrypted by the client, is the size of the intersection.

The second variant enables the server to reveal even less information: just a boolean signifying whether or not the intersection is empty. This could be the perfect solution for a contact tracing application for example. The server simply sums the values as with the previous variant, but then multiplies the sum by a random integer. If the result decrypts to 0 the intersection is empty, otherwise there is overlap between the two sets.

However, a malicious client could quite easily extract Bob’s complete set by sending the right kind of request. For example, Alice could send a request indicating that every element was present in her set and directly infer Bob’s set from the response. Since Alice’s information would be encrypted, Bob would not even be able to detect that Alice was performing this attack. And this will also work against the more restrictive variants if the client sends one request per element in the domain, which will be possible if the domain is small.

Another limitation of this approach is the requirement that every element in the domain needs to be encrypted, transferred from the client to the server, operated on, and transferred back to the client. These requirements scale linearly with the domain size, and are simply impractical for many use cases in terms of computational overhead as well as bandwidth.

### Quiz

1. Which of the following variants are possible with a PSI protocol based on homomorphic encryption?
    - reveal the intersection (correct)
    - reveal only the size of the intersection (correct)
    - reveal only whether or not the intersection is empty (correct)

## A PSI protocol based on hashing

Another option is to use cryptographic hash functions. Bob could simply hash each element in his set and send those hashes to Alice who would hash the elements of her own set and compare those values to the hashes received from Bob to discover the intersection.

This is a bad idea for small domains, because anybody who sees the hashes sent by the server (whether Alice or an eavesdropper) will be able to apply a brute force attack and determine the values which are present in Bob’s set. But for large domains where this kind of attack is not feasible, the approach should be secure.

There is a problem though, which is that Bob has to send a hashed value for every element of his set. This is much better than having to send a value for every element in the entire domain (as with PSI based on homomorphic encryption), but for large sets this could still be an issue. This can be improved by using a Bloom filter as we will see in a later section.

Another limitation of PSI based on hashing is that the more restricted variants are not possible. If Bob wants to reveal only the size of the intersection, or whether it is empty or not, this will not be possible using this technique.

This approach also involves revealing the size of Bob’s set. In some cases this might be acceptable, in other cases it might not.

### Quiz

1. Which of the following variants are possible with a PSI protocol based on hashing?
    - reveal the intersection (correct)
    - reveal only the size of the intersection
    - reveal only whether or not the intersection is empty

## Up next

In the next section we will take a detailed look at a PSI protocol based on Diffie-Hellman key exchange which is more efficient and offers better defences against malicious clients. Then we will implement this Diffie-Hellman PSI protocol.
