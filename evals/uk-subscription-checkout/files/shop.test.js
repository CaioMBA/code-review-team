import test from 'node:test';
import assert from 'node:assert';
import { price, subscribe } from './shop.js';

test('price', () => { assert.equal(price([{ price: 5, qty: 2 }]), 10); });

test('subscribe returns order', async () => {
  const order = await subscribe({ email: 'a@example.com', address: '1 High St' }, { id: 'b1', monthly: 12 }, { marketing: false }, async () => {});
  assert.equal(order.box, 'b1');
});