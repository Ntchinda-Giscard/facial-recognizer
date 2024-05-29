

def lookup_user(index, encoding_list):
    result = index.query(
            namespace="ns1",
            vector=encoding_list,
            top_k=1,
            include_metadata=True,
        )

        # Convert the QueryResponse to a serializable format
    result_data = {
        "matches": [
            {
                "id": match.id,
                "score": match.score,
                "metadata": match.metadata
            }
            for match in result.matches
        ]
    }

    return result_data

