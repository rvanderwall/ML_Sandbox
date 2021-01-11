from flask import Flask

import pandas as pd


def engine_get_recommendations(product_id):
    orders = pd.read_csv("data/OrderHistory.csv")
    orders_for_product = orders[orders.product_id == product_id].order_id.unique()

    # List of orders that have this product
    relevant_orders = orders[orders.order_id.isin(orders_for_product)]

    # Remove this product from relevant orders
    accompanying_products_by_order = relevant_orders[relevant_orders.product_id != id]

    num_instance_by_accompanying_product = accompanying_products_by_order.groupby("product_id")["product_id"].count().reset_index(name="instances")
    # print(num_instance_by_accompanying_product)

    num_orders_for_product = orders_for_product.size
    product_instances = pd.DataFrame(num_instance_by_accompanying_product)
    product_instances["frequency"] = product_instances["instances"]/num_orders_for_product

    recommended_products = pd.DataFrame(product_instances.sort_values("frequency", ascending=False).head(3))

    products = pd.read_csv("data/Products.csv")
    recommended_products = pd.merge(recommended_products, products, on="product_id")
    # print(recommended_products)
    return recommended_products.to_json(orient="table")


app = Flask(__name__)
@app.route("/api/v1.0/recommendations/<int:id>", methods=["GET"])
def get_recommendations(id):
    print(f"product_id: {id}") 
    return engine_get_recommendations(id)


if __name__ == "__main__":
    app.run()

