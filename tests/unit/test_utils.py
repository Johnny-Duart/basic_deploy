from http import HTTPStatus
from unittest.mock import patch

import pytest
from controllers.utils import eleva_quadrado, requires_role


@pytest.mark.parametrize("test_input, expected", [(2, 4), (10, 100), (3, 9)])
def test_elava_quadrado_sucesso(test_input, expected):
    resultado = eleva_quadrado(test_input)
    assert resultado == expected


@pytest.mark.parametrize(
    "test_input, exc_class, msg",
    [
        (
            "a",
            TypeError,
            "unsupported operand type(s) for ** or pow(): 'str' and 'int'",
        ),
        (
            None,
            TypeError,
            "unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'",
        ),
    ],
)
def test_eleva_quadrado_falha(test_input, exc_class, msg):
    with pytest.raises(exc_class) as exc:
        eleva_quadrado(test_input)
    assert str(exc.value) == msg
    assert str(exc.value) == msg


def test_requires_role_success(mocker):

    # Given
    mock_user = mocker.Mock()
    mock_user.role.name = "admin"
    mocker.patch("controllers.utils.get_jwt_identity")
    mocker.patch("controllers.utils.db.get_or_404", return_value=mock_user)
    decorated_function = requires_role("admin")(lambda: "Success")

    # When
    result = decorated_function()

    # Then
    assert result == "Success"


def test_requires_role_fail(mocker):

    # Given
    mock_user = mocker.Mock()
    mock_user.role.name = "normal"
    mocker.patch("controllers.utils.get_jwt_identity")
    mocker.patch("controllers.utils.db.get_or_404", return_value=mock_user)
    decorated_function = requires_role("admin")(lambda: "Success")

    # When
    result, status = decorated_function()

    # Then
    assert status == HTTPStatus.FORBIDDEN
    assert result["message"] == "User dont have acess"
