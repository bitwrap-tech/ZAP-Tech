#!/usr/bin/python3

import pytest

from brownie import accounts


@pytest.fixture(scope="module", autouse=True)
def setup(approve_many, org, share):
    share.mint(org, 100000, {'from': accounts[0]})
    org.setCountry(1, True, 1, (1, 0, 0, 0, 0, 0, 0, 0), {'from': accounts[0]})
    share.transfer(accounts[1], 1000, {'from': accounts[0]})


def test_country_investor_limit_blocked_org_investor(share):
    '''country investor limit - blocked, org to investor'''
    with pytest.reverts("Country Investor Limit"):
        share.transfer(accounts[2], 1000, {'from': accounts[0]})


def test_country_investor_limit_blocked_investor_investor(share):
    '''country investor limit - blocked, investor to investor'''
    with pytest.reverts("Country Investor Limit"):
        share.transfer(accounts[2], 500, {'from': accounts[1]})


def test_country_investor_limit_org_investor(share):
    '''country investor limit - org to existing investor'''
    share.transfer(accounts[1], 1000, {'from': accounts[0]})


def test_country_investor_limit_investor_investor(share):
    '''country investor limit - investor to investor, full balance'''
    share.transfer(accounts[2], 1000, {'from': accounts[1]})


def test_country_investor_limit_investor_investor_different_country(share):
    '''country investor limit, investor to investor, different country'''
    share.transfer(accounts[3], 500, {'from': accounts[1]})


def test_country_investor_limit_rating_blocked_org_investor(kyc, org, share):
    '''country investor limit, rating - blocked, org to investor'''
    org.setCountry(1, True, 1, (0, 1, 0, 0, 0, 0, 0, 0), {'from': accounts[0]})
    kyc.updateInvestor(kyc.getID(accounts[2]), 1, 1, 2000000000, {'from': accounts[0]})
    with pytest.reverts("Country Investor Limit: Rating"):
        share.transfer(accounts[2], 1000, {'from': accounts[0]})


def test_country_investor_limit_rating_blocked_investor_investor(kyc, org, share):
    '''country investor limit, rating - blocked, investor to investor'''
    org.setCountry(1, True, 1, (0, 1, 0, 0, 0, 0, 0, 0), {'from': accounts[0]})
    kyc.updateInvestor(kyc.getID(accounts[2]), 1, 1, 2000000000, {'from': accounts[0]})
    with pytest.reverts("Country Investor Limit: Rating"):
        share.transfer(accounts[2], 500, {'from': accounts[1]})


def test_country_investor_limit_rating_org_investor(org, share):
    '''country investor limit, rating - org to existing investor'''
    org.setCountry(1, True, 1, (0, 1, 0, 0, 0, 0, 0, 0), {'from': accounts[0]})
    share.transfer(accounts[1], 1000, {'from': accounts[0]})


def test_country_investor_limit_rating_investor_investor(org, share):
    '''country investor limit, rating - investor to investor, full balance'''
    org.setCountry(1, True, 1, (0, 1, 0, 0, 0, 0, 0, 0), {'from': accounts[0]})
    share.transfer(accounts[2], 1000, {'from': accounts[1]})


def test_country_investor_limit_rating_investor_investor_different_country(org, share):
    '''country investor limit, rating - investor to investor, different rating'''
    org.setCountry(1, True, 1, (0, 1, 0, 0, 0, 0, 0, 0), {'from': accounts[0]})
    share.transfer(accounts[2], 500, {'from': accounts[1]})
