from extensions import db
from datetime import datetime


class Seller(db.Model):

    __tablename__ = "seller"


    # =========================
    # BASIC
    # =========================

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    # =========================
    # LOGIN
    # =========================

    name = db.Column(
        db.String(100),
        nullable=False
    )


    phone = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )


    email = db.Column(
        db.String(150),
        unique=True
    )


    password = db.Column(
        db.String(200),
        nullable=False
    )



    # =========================
    # SHOP INFO
    # =========================

    shop_name = db.Column(
        db.String(200),
        nullable=False
    )


    shop_description = db.Column(
        db.Text
    )


    shop_logo = db.Column(
        db.String(500)
    )


    address = db.Column(
        db.String(300)
    )


    city = db.Column(
        db.String(100)
    )



    # =========================
    # BALANCE
    # =========================

    balance = db.Column(
        db.Integer,
        default=0
    )


    total_income = db.Column(
        db.Integer,
        default=0
    )


    withdrawn_money = db.Column(
        db.Integer,
        default=0
    )


    pending_withdraw = db.Column(
        db.Integer,
        default=0
    )



    # =========================
    # SALES
    # =========================

    total_sales = db.Column(
        db.Integer,
        default=0
    )


    sold_products = db.Column(
        db.Integer,
        default=0
    )


    total_orders = db.Column(
        db.Integer,
        default=0
    )


    commission = db.Column(
        db.Integer,
        default=10
    )



    # =========================
    # SHOP RATING
    # =========================

    rating = db.Column(
        db.Float,
        default=0
    )


    reviews_count = db.Column(
        db.Integer,
        default=0
    )



    # =========================
    # STATUS
    # =========================

    status = db.Column(
        db.String(50),
        default="pending"
    )


    verified = db.Column(
        db.Boolean,
        default=False
    )


    blocked_reason = db.Column(
        db.Text
    )



    # =========================
    # TIME
    # =========================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    last_login = db.Column(
        db.DateTime
    )


    last_activity = db.Column(
        db.DateTime
    )



    # =========================
    # RELATIONSHIPS
    # =========================


    products = db.relationship(
        "Product",
        back_populates="seller",
        cascade="all, delete-orphan"
    )


    order_items = db.relationship(
        "OrderItem",
        back_populates="seller",
        cascade="all, delete-orphan"
    )


    withdraw_requests = db.relationship(
        "WithdrawRequest",
        back_populates="seller",
        cascade="all, delete-orphan"
    )


    notifications = db.relationship(
        "Notification",
        back_populates="seller",
        cascade="all, delete-orphan"
    )



    # =========================
    # FUNCTIONS
    # =========================


    def add_income(self, amount):

        self.balance += amount

        self.total_income += amount



    def withdraw_request(self, amount):

        if self.balance >= amount:

            self.pending_withdraw += amount

            return True

        return False



    def complete_withdraw(self, amount):

        if self.balance >= amount:

            self.balance -= amount

            self.withdrawn_money += amount

            self.pending_withdraw -= amount

            return True

        return False



    def add_sale(
        self,
        price,
        quantity=1
    ):

        self.total_sales += price

        self.sold_products += quantity

        self.total_orders += 1



    def calculate_commission(
        self,
        amount
    ):

        fee = (
            amount
            *
            self.commission
            /
            100
        )

        return amount - fee



    def update_rating(self):

        if self.reviews_count:

            pass



    def activate(self):

        self.status = "active"

        self.verified = True



    def block(self, reason):

        self.status = "blocked"

        self.blocked_reason = reason



    def __repr__(self):

        return f"<Seller {self.shop_name}>"


    remember_token = db.Column(
    db.String(255),
    nullable=True
)

# =========================
# ADMIN CONTROL
# =========================

is_blocked = db.Column(
    db.Boolean,
    default=False
)

bonus_received = db.Column(
    db.Integer,
    default=0
)


# =========================
# BALANCE ACTION
# =========================

def add_balance(self, amount):

    self.balance += amount
    self.total_income += amount



def give_bonus(self, amount):

    self.balance += amount
    self.bonus_received += amount



def withdraw_money(self, amount):

    if self.balance >= amount:

        self.balance -= amount
        self.withdrawn_money += amount

        return True

    return False



def block_seller(self):

    self.status="blocked"
    self.is_blocked=True



def unblock_seller(self):

    self.status="active"
    self.is_blocked=False