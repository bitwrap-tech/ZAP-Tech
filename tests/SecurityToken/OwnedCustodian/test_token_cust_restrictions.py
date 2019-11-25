#!/usr/bin/python3

import pytest

from brownie import accounts


@pytest.fixture(scope="module", autouse=True)
def setup(approve_many, org, share, cust):
    share.mint(org, 100000, {'from': accounts[0]})
    share.transfer(accounts[2], 1000, {'from': accounts[0]})
    share.transfer(cust, 500, {'from': accounts[0]})
    share.transfer(cust, 500, {'from': accounts[2]})
    org.setEntityRestriction(cust.ownerID(), True, {'from': accounts[0]})


def test_from_org(share, cust):
    '''restricted custodian - org to custodian'''
    with pytest.reverts("Receiver restricted: Issuer"):
        share.transfer(cust, 1000, {'from': accounts[0]})


def test_from_investor(share, cust):
    '''restricted custodian - investor to custodian'''
    with pytest.reverts("Receiver restricted: Issuer"):
        share.transfer(cust, 1000, {'from': accounts[2]})


def test_transferInternal(share, cust):
    '''restricted custodian - internal transfer'''
    with pytest.reverts("Authority restricted"):
        cust.transferInternal(share, accounts[2], accounts[3], 500, {'from': accounts[0]})


def test_to_org(share, cust):
    '''restricted custodian - to org'''
    with pytest.reverts("Sender restricted: Issuer"):
        cust.transfer(share, accounts[0], 500, {'from': accounts[0]})


def test_to_investor(share, cust):
    '''restricted custodian - to investor'''
    with pytest.reverts("Sender restricted: Issuer"):
        cust.transfer(share, accounts[2], 500, {'from': accounts[0]})


def test_org_transferFrom(share, cust):
    '''restricted custodian - org transfer out with transferFrom'''
    share.transferFrom(cust, accounts[2], 500, {'from': accounts[0]})
