from private_set_intersection import PSIClient, PSIServer


test_cases = [
    # (client_set, intersection)
    ([], []),
    ([1], [1]),
    ([1, 6], [1]),
    ([6, 7], []),
    ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
    ([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5]),
]


def test_private_set_intersection():
    modulus = 35317
    server_set = set([1, 2, 3, 4, 5])

    for test_case in test_cases:
        client_set, intersection = test_case

        server = PSIServer(server_set, modulus)
        client = PSIClient(client_set, modulus)

        client_intermediate_keys = client.prepare_intermediate_keys()
        client_keys, server_intermediate_keys = server.handle_request(
            client_intermediate_keys
        )
        result = client.handle_response(client_keys, server_intermediate_keys)

        assert result == intersection
