from app.resources.transaction import create_transaction
from app.models import RecurrentTransactionModel
from app.db import db
from app.factory.create_app import create_app

import datetime
from typing import List

app = create_app()


def create_recurrent_transaction():
    with app.app_context():
        today_transactions: List[RecurrentTransactionModel] = (RecurrentTransactionModel.query.filter_by(
                                                                next_transaction=datetime.datetime.now().date())
                                                               .all())
        if not today_transactions:
            return

        for r_t_data in today_transactions:
            transaction_data = {
                "type": r_t_data.type,
                "category_id": r_t_data.category_id,
                "amount": r_t_data.amount,
                "description": r_t_data.description
            }
            create_transaction(transaction_data, user_id=r_t_data.user_id)
            r_t_data.next_transaction = r_t_data.next_transaction + datetime.timedelta(days=30)
            db.session.add(r_t_data)
            db.session.commit()


if __name__ == '__main__':
    create_recurrent_transaction()
