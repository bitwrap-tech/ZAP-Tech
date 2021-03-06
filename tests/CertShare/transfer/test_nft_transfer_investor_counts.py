#!/usr/bin/python3

import pytest

from brownie import accounts


@pytest.fixture(scope="module", autouse=True)
def setup(org, nft):
    nft.mint(org, 100000, 0, "0x00", {"from": accounts[0]})


def test_org_to_member(check_counts, nft):
    """member counts - org/member transfers"""
    check_counts()
    nft.transfer(accounts[1], 1000, {"from": accounts[0]})
    check_counts(one=(1, 1, 0))
    nft.transfer(accounts[1], 1000, {"from": accounts[0]})
    nft.transfer(accounts[2], 1000, {"from": accounts[0]})
    nft.transfer(accounts[3], 1000, {"from": accounts[0]})
    check_counts(one=(2, 1, 1), two=(1, 1, 0))
    nft.transfer(accounts[1], 96000, {"from": accounts[0]})
    check_counts(one=(2, 1, 1), two=(1, 1, 0))
    nft.transfer(accounts[0], 1000, {"from": accounts[1]})
    check_counts(one=(2, 1, 1), two=(1, 1, 0))
    nft.transfer(accounts[0], 97000, {"from": accounts[1]})
    check_counts(one=(1, 0, 1), two=(1, 1, 0))
    nft.transfer(accounts[0], 1000, {"from": accounts[2]})
    nft.transfer(accounts[0], 1000, {"from": accounts[3]})
    check_counts()


def test_member_to_member(check_counts, nft):
    """member counts - member/member transfers"""
    nft.transfer(accounts[1], 1000, {"from": accounts[0]})
    nft.transfer(accounts[2], 1000, {"from": accounts[0]})
    nft.transfer(accounts[3], 1000, {"from": accounts[0]})
    nft.transfer(accounts[4], 1000, {"from": accounts[0]})
    nft.transfer(accounts[5], 1000, {"from": accounts[0]})
    nft.transfer(accounts[6], 1000, {"from": accounts[0]})
    check_counts(one=(2, 1, 1), two=(2, 1, 1), three=(2, 1, 1))
    nft.transfer(accounts[2], 500, {"from": accounts[1]})
    check_counts(one=(2, 1, 1), two=(2, 1, 1), three=(2, 1, 1))
    nft.transfer(accounts[2], 500, {"from": accounts[1]})
    check_counts(one=(1, 0, 1), two=(2, 1, 1), three=(2, 1, 1))
    nft.transfer(accounts[3], 2000, {"from": accounts[2]})
    check_counts(two=(2, 1, 1), three=(2, 1, 1))
    nft.transfer(accounts[3], 1000, {"from": accounts[4]})
    check_counts(two=(1, 1, 0), three=(2, 1, 1))
    nft.transfer(accounts[4], 500, {"from": accounts[3]})
    check_counts(two=(2, 1, 1), three=(2, 1, 1))
