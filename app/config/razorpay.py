import razorpay

from app.config.secretes import secretes


class RazorPay:

    def __init__(self):
        self.client = razorpay.Client(
            auth=(
                secretes.RAZOR_PAY_KEY,
                secretes.RAZOR_PAY_SECRET
            )
        )

    def generate_payment_link(
        self,
        amount: int,
        description: str,
        reference_id: str,
        user_id: int,
        callback_url: str = None
    ):
        data = {
            "amount": amount * 100,    #Examp ₹500 -> 50000 paise
            "currency": "INR",
            "description": description,
            "reference_id": reference_id,
            

            "customer": {
                "user_id": user_id,
            },

            "notify": {
                'sms': True,
                'email': True
            },

            "reminder_enable": True
        }

        if secretes.RAZOR_CALLBACK_URL:
          data["callback_url"] = secretes.RAZOR_CALLBACK_URL
          data["callback_method"] = "get"

        return self.client.payment_link.create(data)


    def get_payment_link(self, payment_link_id: str):
        return self.client.payment_link.fetch(payment_link_id)

    def cancel_payment_link(self, payment_link_id: str):
        return self.client.payment_link.cancel(payment_link_id)

    def get_payment(self, payment_id: str):
        return self.client.payment.fetch(payment_id)

    def refund_payment(self, payment_id: str):
        return self.client.payment.refund(payment_id)

razorpay = RazorPay()
