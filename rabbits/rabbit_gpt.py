from dataclasses import dataclass


@dataclass
class GptApiPrice:
    PRICES = {
        "gpt-5": (1.25, 10),
        "gpt-5-mini": (0.25, 2),
        "gpt-5-nano": (0.05, 0.4),
        "gpt-4.1": (2, 8),
        "gpt-4.1-mini": (0.4, 1.6),
        "gpt-4.1-nano": (0.1, 0.4),
        "gpt-4o": (2.5, 10),
        "gpt-4o-mini": (0.15, 0.6),
    }

    @classmethod
    def compute_price(cls, openai_model: str, if_batch: bool, input_token: int, output_token: int | None) -> dict:
        if output_token is None:
            print("No output token number is given. "
                  "We default the output token number to the same as the input token number.")
            output_token_est = input_token
        else:
            output_token_est = output_token

        if openai_model not in cls.PRICES:
            raise ValueError(f"Unrecognized model name: {openai_model}")

        input_price, output_price = cls.PRICES[openai_model]

        if if_batch is True:
            print("Computation will be based on batch API price")
            input_price = input_price / 2
            output_price = output_price / 2

        input_cost = (input_token / 1000000) * input_price
        output_cost = (output_token_est / 1000000) * output_price
        total_cost = input_cost + output_cost
        return {
            "model_name": openai_model,
            "input_token": input_token,
            "output_token": output_token,
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": total_cost
        }
