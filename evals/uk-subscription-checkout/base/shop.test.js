import test from 'node:test';
import assert from 'node:assert';
import { price } from './shop.js';

test('price', () => { assert.equal(price([{ price: 5, qty: 2 }]), 10); });
