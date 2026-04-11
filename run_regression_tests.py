import unittest
from logic_gate import intercept_payload

test_cases = [
    # 用例1：valid - 数字和source都匹配
    {
        "USD": "200M",
        "percentage": "25%",
        "context": "This is a claim from Reuters about the shipment disruption of $200 million, which accounts for 25% of total export volume.",
        "source": "Reuters",
        "expected_result": "valid"
    },
    # 用例2：intercepted - percentage不匹配
    {
        "USD": "200M",
        "percentage": "25%",
        "context": "This is a claim from Reuters about the shipment disruption of $200 million.",
        "source": "Reuters",
        "expected_result": "intercepted"
    },
    # 用例3：intercepted - source不匹配
    {
        "USD": "500K",
        "percentage": "10%",
        "context": "Local media reports a shipment disruption with a value of $500,000, affecting 10% of local supplies.",
        "source": "CNN",
        "expected_result": "intercepted"
    },
    # 用例4：valid - 数字（含percent格式）和source都匹配
    {
        "USD": "500K",
        "percentage": "10%",
        "context": "CNN reports a shipment disruption with a value of $500,000, affecting 10 percent of local supplies.",
        "source": "CNN",
        "expected_result": "valid"
    }
]

class TestLogicGate(unittest.TestCase):
    def test_all_cases(self):
        for idx, case in enumerate(test_cases):
            with self.subTest(case_idx=idx, case_desc=f"{case['expected_result']} case"):
                result = intercept_payload(case)
                self.assertEqual(result['status'], case['expected_result'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
