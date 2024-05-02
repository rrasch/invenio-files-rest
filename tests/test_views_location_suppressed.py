# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test location related views."""

import pytest
from flask import json, url_for
from testutils import login_user

from invenio_files_rest.models import Bucket


def get_json(resp):
    """Get JSON from response."""
    return json.loads(resp.get_data(as_text=True))


@pytest.mark.parametrize(
    "user, expected",
    [
        (None, 401),
        ("auth", 403),
        ("location", 200),
    ],
)
def test_post_bucket(app, client, headers, dummy_location, permissions, user, expected):
    """Test post a bucket."""
    expected_keys = [
        "id",
        "links",
        "size",
        "quota_size",
        "max_file_size",
        "locked",
        "created",
        "updated",
    ]

    params = [{}, {"location": dummy_location.name}, {"location": "suppressed"}]

    login_user(client, permissions[user])

    for data in params:
        json_data = json.dumps(data)
        resp = client.post(
            url_for("invenio_files_rest.location_api"), data=json_data, headers=headers
        )
        assert resp.status_code == expected
        if resp.status_code == 200:
            resp_json = get_json(resp)
            for key in expected_keys:
                assert key in resp_json
            assert Bucket.get(resp_json["id"])


@pytest.mark.parametrize(
    "user, expected",
    [
        (None, 401),
        ("auth", 403),
        ("location", 404),
    ],
)
def test_post_bucket_unknown_location(
    app, client, headers, permissions, user, expected
):
    """Test post a bucket with unknown location."""

    params = [{"location": "unknown"}]

    login_user(client, permissions[user])

    for data in params:
        json_data = json.dumps(data)
        resp = client.post(
            url_for("invenio_files_rest.location_api"), data=json_data, headers=headers
        )
        assert resp.status_code == expected
