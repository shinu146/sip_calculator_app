import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calculate_and_plot_sip_with_increase(rate, years, initial_sip, sip_increase_rate, initial_investment):
    monthly_rate = (1 + rate) ** (1/12) - 1
    monthly_sip_increase = (1 + sip_increase_rate) ** (1/12) - 1
    months = years * 12
    
    portfolio_values = np.zeros(months + 1)
    total_invested = np.zeros(months + 1)
    sip_amounts = np.zeros(months + 1)
    
    portfolio_values[0] = initial_investment
    total_invested[0] = initial_investment
    sip_amounts[0] = initial_sip
    
    for i in range(1, months + 1):
        sip_amounts[i] = sip_amounts[i-1] * (1 + monthly_sip_increase)
        portfolio_values[i] = (portfolio_values[i-1] + sip_amounts[i]) * (1 + monthly_rate)
        total_invested[i] = total_invested[i-1] + sip_amounts[i]
    
    time = np.arange(months + 1) / 12
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(time, portfolio_values, label='Portfolio Value')
    ax1.plot(time, total_invested, label='Total Invested')
    ax1.set_xlabel('Years')
    ax1.set_ylabel('Amount')
    ax1.set_title('SIP Investment Growth with Annual Increase')
    ax1.legend(loc='upper left')
    ax1.grid(True)
    
    ax2 = ax1.twinx()
    ax2.plot(time, sip_amounts, 'r--', label='Monthly SIP Amount')
    ax2.set_ylabel('Monthly SIP Amount', color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    ax2.legend(loc='lower right')
    
    plt.tight_layout()
    
    return portfolio_values[-1], total_invested[-1], sip_amounts[-1], fig

st.title('SIP Investment Calculator')

rate = st.number_input('Annual Rate of Return (%)', min_value=0.0, max_value=100.0, value=12.0, step=0.1) / 100
years = st.number_input('Investment Duration (Years)', min_value=1, max_value=50, value=10, step=1)
initial_sip = st.number_input('Initial Monthly SIP Amount', min_value=100, max_value=1000000, value=1000, step=100)
sip_increase_rate = st.number_input('Annual SIP Increase Rate (%)', min_value=0.0, max_value=100.0, value=5.0, step=0.1) / 100
initial_investment = st.number_input('Initial Investment', min_value=0, max_value=10000000, value=10000, step=1000)

if st.button('Calculate'):
    final_value, total_invested, final_sip, fig = calculate_and_plot_sip_with_increase(
        rate, years, initial_sip, sip_increase_rate, initial_investment
    )
    
    st.write(f"Final portfolio value: ₹{final_value:,.2f}")
    st.write(f"Total amount invested: ₹{total_invested:,.2f}")
    st.write(f"Final monthly SIP amount: ₹{final_sip:,.2f}")
    
    st.pyplot(fig)

st.write("Note: This calculator assumes that returns are compounded monthly and the SIP amount increases annually.")