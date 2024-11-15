from datetime import datetime

import pytest
from .test_order import assert_contract_order

def test_futures_ping(futuresClient):
    futuresClient.futures_ping()


def test_futures_time(futuresClient):
    futuresClient.futures_time()


def test_futures_exchange_info(futuresClient):
    futuresClient.futures_exchange_info()


def test_futures_order_book(futuresClient):
    futuresClient.futures_order_book(symbol="BTCUSDT")


def test_futures_recent_trades(futuresClient):
    futuresClient.futures_recent_trades(symbol="BTCUSDT")


def test_futures_historical_trades(futuresClient):
    futuresClient.futures_historical_trades(symbol="BTCUSDT")


def test_futures_aggregate_trades(futuresClient):
    futuresClient.futures_aggregate_trades(symbol="BTCUSDT")


def test_futures_klines(futuresClient):
    futuresClient.futures_klines(symbol="BTCUSDT", interval="1h")


def test_futures_continous_klines(futuresClient):
    futuresClient.futures_continous_klines(pair="BTCUSDT", contractType="PERPETUAL", interval="1h")


def test_futures_historical_klines(futuresClient):
    futuresClient.futures_historical_klines(symbol="BTCUSDT", interval="1h", start_str=datetime.now().strftime("%Y-%m-%d"))


def test_futures_historical_klines_generator(futuresClient):
    futuresClient.futures_historical_klines_generator(symbol="BTCUSDT", interval="1h", start_str=datetime.now().strftime("%Y-%m-%d"))


def test_futures_mark_price(futuresClient):
    futuresClient.futures_mark_price()


def test_futures_funding_rate(futuresClient):
    futuresClient.futures_funding_rate()


@pytest.mark.skip(reason="Not implemented")
def test_futures_top_longshort_account_ratio(futuresClient):
    futuresClient.futures_top_longshort_account_ratio()


@pytest.mark.skip(reason="Not implemented")
def test_futures_top_longshort_position_ratio(futuresClient):
    futuresClient.futures_top_longshort_position_ratio()


@pytest.mark.skip(reason="Not implemented")
def test_futures_global_longshort_ratio(futuresClient):
    futuresClient.futures_global_longshort_ratio()


def test_futures_ticker(futuresClient):
    futuresClient.futures_ticker()


def test_futures_symbol_ticker(futuresClient):
    futuresClient.futures_symbol_ticker()


def test_futures_orderbook_ticker(futuresClient):
    futuresClient.futures_orderbook_ticker()


def test_futures_liquidation_orders(futuresClient):
    futuresClient.futures_liquidation_orders()


def test_futures_api_trading_status(futuresClient):
    futuresClient.futures_api_trading_status()


def test_futures_commission_rate(futuresClient):
    futuresClient.futures_commission_rate(symbol="BTCUSDT")


def test_futures_adl_quantile_estimate(futuresClient):
    futuresClient.futures_adl_quantile_estimate()


def test_futures_open_interest(futuresClient):
    futuresClient.futures_open_interest(symbol="BTCUSDT")


def test_futures_index_info(futuresClient):
    futuresClient.futures_index_info()


@pytest.mark.skip(reason="Not implemented")
def test_futures_open_interest_hist(futuresClient):
    futuresClient.futures_open_interest_hist(symbol="BTCUSDT")


def test_futures_leverage_bracket(futuresClient):
    futuresClient.futures_leverage_bracket()


@pytest.mark.skip(reason="Not implemented")
def test_futures_account_transfer(futuresClient):
    futuresClient.futures_account_transfer()

@pytest.mark.skip(reason="Not implemented")
def test_transfer_history(client):
    client.transfer_history()

@pytest.mark.skip(reason="Not implemented")
def test_futures_loan_borrow_history(futuresClient):
    futuresClient.futures_loan_borrow_history()


@pytest.mark.skip(reason="Not implemented")
def test_futures_loan_repay_history(futuresClient):
    futuresClient.futures_loan_repay_history()

@pytest.mark.skip(reason="Not implemented")
def test_futures_loan_wallet(futuresClient):
    futuresClient.futures_loan_wallet()


@pytest.mark.skip(reason="Not implemented")
def test_futures_cross_collateral_adjust_history(futuresClient):
    futuresClient.futures_cross_collateral_adjust_history()


@pytest.mark.skip(reason="Not implemented")
def test_futures_cross_collateral_liquidation_history(futuresClient):
    futuresClient.futures_cross_collateral_liquidation_history()


@pytest.mark.skip(reason="Not implemented")
def test_futures_loan_interest_history(futuresClient):
    futuresClient.futures_loan_interest_history()


def test_futures_create_get_edit_cancel_order(futuresClient):
    ticker = futuresClient.futures_ticker(symbol="LTCUSDT")
    positions = futuresClient.futures_position_information(symbol="LTCUSDT")
    order = futuresClient.futures_create_order(
        symbol=ticker["symbol"],
        side="BUY",
        positionSide=positions[0]["positionSide"],
        type="LIMIT",
        timeInForce="GTC",
        quantity=0.1,
        price=str(round(float(ticker["lastPrice"]) - 1)),
    )
    assert_contract_order(futuresClient, order)
    order = futuresClient.futures_modify_order(
        orderid=order["orderId"],
        symbol=order["symbol"],
        quantity=0.11,
        side=order["side"],
        price=order["price"],
    )
    assert_contract_order(futuresClient, order)
    order = futuresClient.futures_get_order(
        symbol=order["symbol"], orderid=order["orderId"]
    )
    assert_contract_order(futuresClient, order)
    order = futuresClient.futures_cancel_order(
        orderid=order["orderId"], symbol=order["symbol"]
    )


def test_futures_create_test_order(futuresClient):
    ticker = futuresClient.futures_ticker(symbol="LTCUSDT")
    positions = futuresClient.futures_position_information(symbol="LTCUSDT")
    futuresClient.futures_create_test_order(
        symbol=ticker["symbol"],
        side="BUY",
        positionSide=positions[0]["positionSide"],
        type="LIMIT",
        timeInForce="GTC",
        quantity=0.1,
        price=str(round(float(ticker["lastPrice"]) - 1)),
    )


def test_futures_place_batch_order_and_cancel(futuresClient):
    ticker = futuresClient.futures_ticker(symbol="LTCUSDT")
    positions = futuresClient.futures_position_information(symbol="LTCUSDT")
    orders =futuresClient.futures_place_batch_order(
        batchOrders=[{
            "symbol": ticker["symbol"],
            "side": "BUY",
            "positionSide": positions[0]["positionSide"],
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": '0.1',
            "price": str(round(float(ticker["lastPrice"]) - 1)),
        }]
    )
    for order in orders:
        assert_contract_order(futuresClient, order)

    order_ids = [order["orderId"] for order in orders]
    # orders = futuresClient.futures_cancel_orders(symbol=orders[0]["symbol"], orderidList=order_ids)
    # for order in orders:
    #     assert_contract_order(futuresClient, order)


def test_futures_get_open_orders(futuresClient):
    futuresClient.futures_get_open_orders()


def test_futures_get_all_orders(futuresClient):
    orders=futuresClient.futures_get_all_orders()
    print(orders)


def test_futures_cancel_all_open_orders(futuresClient):
    futuresClient.futures_cancel_all_open_orders(symbol="LTCUSDT")




def test_futures_countdown_cancel_all(futuresClient):
    futuresClient.futures_countdown_cancel_all(symbol="LTCUSDT", countdownTime=10)


def test_futures_account_balance(futuresClient):
    futuresClient.futures_account_balance()


def test_futures_account(futuresClient):
    futuresClient.futures_account()


def test_futures_change_leverage(futuresClient):
    futuresClient.futures_change_leverage(symbol="LTCUSDT", leverage=10)


def test_futures_change_margin_type(futuresClient):
    try:
        futuresClient.futures_change_margin_type(symbol="XRPUSDT", marginType="CROSSED")
    except Exception as e:
        futuresClient.futures_change_margin_type(symbol="XRPUSDT", marginType="ISOLATED")


def test_futures_position_margin_history(futuresClient):
    position = futuresClient.futures_position_margin_history(symbol="LTCUSDT")
    print(position)

def test_futures_position_information(futuresClient):
    futuresClient.futures_position_information()


def test_futures_account_trades(futuresClient):
    futuresClient.futures_account_trades()


def test_futures_income_history(futuresClient):
    futuresClient.futures_income_history()


def close_all_futures_positions(futuresClient):
    # Get all open positions
    positions = futuresClient.futures_position_information(symbol="LTCUSDT")

    for position in positions:
        # Check if there is an open position
        if float(position['positionAmt']) != 0:
            symbol = position['symbol']
            position_amt = float(position['positionAmt'])
            side = "SELL" if position_amt > 0 else "BUY"

            # Place a market order to close the position
            try:
                print(f"Closing position for {symbol}: {position_amt} units")
                futuresClient.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type="market",
                    quantity=abs(position_amt)
                )
                print(f"Position for {symbol} closed successfully.")
            except Exception as e:
                print(f"Failed")


def test_futures_get_and_change_position_mode(futuresClient):
    mode = futuresClient.futures_get_position_mode()
    futuresClient.futures_change_position_mode(dualSidePosition=not mode['dualSidePosition'])

@pytest.mark.skip(reason="Not implemented")
def test_futures_change_multi_assets_mode(futuresClient):
    futuresClient.futures_change_multi_assets_mode()


def test_futures_get_multi_assets_mode(futuresClient):
    futuresClient.futures_get_multi_assets_mode()


def test_futures_stream_get_listen_key(futuresClient):
    futuresClient.futures_stream_get_listen_key()


@pytest.mark.skip(reason="Not implemented")
def test_futures_stream_close(futuresClient):
    futuresClient.futures_stream_close()


# new methods
def test_futures_account_config(futuresClient):
    futuresClient.futures_account_config()


def test_futures_symbol_config(futuresClient):
    futuresClient.futures_symbol_config()


# COIN Futures API
def test_futures_coin_ping(futuresClient):
    futuresClient.futures_coin_ping()


def test_futures_coin_time(futuresClient):
    futuresClient.futures_coin_time()


def test_futures_coin_exchange_info(futuresClient):
    futuresClient.futures_coin_exchange_info()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_order_book(futuresClient):
    futuresClient.futures_coin_order_book()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_recent_trades(futuresClient):
    futuresClient.futures_coin_recent_trades()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_historical_trades(futuresClient):
    futuresClient.futures_coin_historical_trades()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_aggregate_trades(futuresClient):
    futuresClient.futures_coin_aggregate_trades()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_klines(futuresClient):
    futuresClient.futures_coin_klines()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_continous_klines(futuresClient):
    futuresClient.futures_coin_continous_klines()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_index_price_klines(futuresClient):
    futuresClient.futures_coin_index_price_klines()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_mark_price_klines(futuresClient):
    futuresClient.futures_coin_mark_price_klines()


def test_futures_coin_mark_price(futuresClient):
    futuresClient.futures_coin_mark_price()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_funding_rate(futuresClient):
    futuresClient.futures_coin_funding_rate()


def test_futures_coin_ticker(futuresClient):
    futuresClient.futures_coin_ticker()


def test_futures_coin_symbol_ticker(futuresClient):
    futuresClient.futures_coin_symbol_ticker()


def test_futures_coin_orderbook_ticker(futuresClient):
    futuresClient.futures_coin_orderbook_ticker()


def test_futures_coin_liquidation_orders(futuresClient):
    futuresClient.futures_coin_liquidation_orders()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_open_interest(futuresClient):
    futuresClient.futures_coin_open_interest()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_open_interest_hist(futuresClient):
    futuresClient.futures_coin_open_interest_hist()


def test_futures_coin_leverage_bracket(futuresClient):
    futuresClient.futures_coin_leverage_bracket()


@pytest.mark.skip(reason="Not implemented")
def test_new_transfer_history(futuresClient):
    futuresClient.new_transfer_history()


@pytest.mark.skip(reason="Not implemented")
def test_funding_wallet(futuresClient):
    futuresClient.funding_wallet()


@pytest.mark.skip(reason="Not implemented")
def test_get_user_asset(futuresClient):
    futuresClient.get_user_asset()


@pytest.mark.skip(reason="Not implemented")
def test_universal_transfer(futuresClient):
    futuresClient.universal_transfer()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_create_order(futuresClient):
    futuresClient.futures_coin_create_order()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_place_batch_order(futuresClient):
    futuresClient.futures_coin_place_batch_order()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_get_order(futuresClient):
    futuresClient.futures_coin_get_order()


def test_futures_coin_get_open_orders(futuresClient):
    futuresClient.futures_coin_get_open_orders()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_get_all_orders(futuresClient):
    futuresClient.futures_coin_get_all_orders()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_cancel_order(futuresClient):
    futuresClient.futures_coin_cancel_order()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_cancel_all_open_orders(futuresClient):
    futuresClient.futures_coin_cancel_all_open_orders()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_cancel_orders(futuresClient):
    futuresClient.futures_coin_cancel_orders()


def test_futures_coin_account_balance(futuresClient):
    futuresClient.futures_coin_account_balance()


def test_futures_coin_account(futuresClient):
    futuresClient.futures_coin_account()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_change_leverage(futuresClient):
    futuresClient.futures_coin_change_leverage(symbol="XRPUSDT", leverage=10)


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_change_margin_type(futuresClient):
    futuresClient.futures_coin_change_margin_type()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_change_position_margin(futuresClient):
    futuresClient.futures_coin_change_position_margin()


def test_futures_coin_position_margin_history(futuresClient):
    futuresClient.futures_coin_position_margin_history()


def test_futures_coin_position_information(futuresClient):
    futuresClient.futures_coin_position_information()


def test_futures_coin_account_trades(futuresClient):
    futuresClient.futures_coin_account_trades()


def test_futures_coin_income_history(futuresClient):
    futuresClient.futures_coin_income_history()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_change_position_mode(futuresClient):
    futuresClient.futures_coin_change_position_mode()


def test_futures_coin_get_position_mode(futuresClient):
    futuresClient.futures_coin_get_position_mode()


def test_futures_coin_stream_close(futuresClient):
    listen_key = futuresClient.futures_coin_stream_get_listen_key()
    futuresClient.futures_coin_stream_close(listenKey=listen_key)


@pytest.mark.skip(reason="Not implemented")
def test_get_all_coins_info(futuresClient):
    futuresClient.get_all_coins_info()


@pytest.mark.skip(reason="Not implemented")
def test_get_account_snapshot(futuresClient):
    futuresClient.get_account_snapshot()


@pytest.mark.skip(reason="Not implemented")
def test_disable_fast_withdraw_switch(futuresClient):
    futuresClient.disable_fast_withdraw_switch()


@pytest.mark.skip(reason="Not supported in testnet")
def test_enable_fast_withdraw_switch(futuresClient):
    futuresClient.enable_fast_withdraw_switch()