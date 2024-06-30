This repo contains source code for the Medium article [What I've learned trying to recreate Apache Beam](https://conalldalydev.medium.com/what-ive-learned-trying-to-recreate-apache-beam-4a95a9f4ba6d) and contains code for building data pipelines using similar syntax to Apache Beam without the need for a runner.

It includes examples of how to build DAGs, implement Filter and GroupBy transforms, apply labels to transforms and overload Python operators.

Please refer to `test_transforms.py` to see working implementation of all of the above.

```
def test_group_by_into_transform(self):
    p = Pipeline()
    p | Create(["strawberry", "banana", "blueberry"]) | GroupBy() | GroupCount()

    results = p.run()

    expected = [{'key': 's', 'values': ['strawberry'], 'length': 1},
                {'key': 'b', 'values': ['banana', 'blueberry'], 'length': 2}]

    self.assertEqual(expected, results)
```

