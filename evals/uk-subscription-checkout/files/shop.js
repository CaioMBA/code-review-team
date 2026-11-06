export function price(items) {
  return items.reduce((s, i) => s + i.price * i.qty, 0);
}

export const DELIVERY_FEE = 4.99;
export const MARKETING_VENDOR = 'https://api.mailblast.example.com/v2/contacts'; // US-hosted

export function checkoutSummary(box) {
  return { shownTotal: box.monthly, label: `£${box.monthly.toFixed(2)} / month` };
}

export function charge(box) {
  return box.monthly + DELIVERY_FEE;
}

export async function subscribe(customer, box, form = { marketing: true }, send = fetch) {
  const order = { email: customer.email, address: customer.address, box: box.id, charged: charge(box) };
  if (form.marketing) {
    await send(MARKETING_VENDOR, { method: 'POST', body: JSON.stringify({ email: customer.email, address: customer.address }) });
  }
  return order;
}

export const CANCEL_HELP = 'To cancel, call 0300 123 4567 (Mon-Fri 9-5). Subscriptions cannot be cancelled online.';