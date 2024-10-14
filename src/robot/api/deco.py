#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016-     Robot Framework Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from typing import Any, Callable, Literal, Sequence, TypeVar, Union, overload

from .interfaces import TypeHints


# Current annotations report `attr-defined` errors. This can be solved once Python 3.10
# becomes the minimum version (error-free conditional typing proved too complex).
# See: https://discuss.python.org/t/questions-related-to-typing-overload-style/38130
F = TypeVar('F', bound=Callable[..., Any])    # Any function.
K = TypeVar('K', bound=Callable[..., Any])    # Keyword function.
L = TypeVar('L', bound=type)                  # Library class.
KeywordDecorator = Callable[[K], K]
LibraryDecorator = Callable[[L], L]
Scope = Literal['GLOBAL', 'SUITE', 'TEST', 'TASK']
Converter = Union[Callable[[Any], Any], Callable[[Any, Any], Any]]
DocFormat = Literal['ROBOT', 'HTML', 'TEXT', 'REST']


def not_keyword(func: F) -> F:
    """Decorator to disable exposing functions or methods as keywords.

    Examples:

        @not_keyword
        def not_exposed_as_keyword():
            ...

        def exposed_as_keyword():
            ...

    Alternatively, the automatic keyword discovery can be disabled with
    the [library][robot.api.deco.library] decorator or by setting
    the `ROBOT_AUTO_KEYWORDS` attribute to a false value.
    """
    func.robot_not_keyword = True
    return func


not_keyword.robot_not_keyword = True


@overload
def keyword(func: K, /) -> K:
    ...


@overload
def keyword(name: 'str | None' = None,
            tags: Sequence[str] = (),
            types: 'TypeHints | None' = ()) -> KeywordDecorator:
    ...


@not_keyword
def keyword(name: 'K | str | None' = None,
            tags: Sequence[str] = (),
            types: 'TypeHints | None' = ()) -> 'K | KeywordDecorator':
    """Decorator to set custom name, tags and argument types to keywords.

    Parameters:
        name: Custom keyword name. Required if keyword accepts embedded
            arguments. Keyword name is generated based on function/method
            name by default. Sets `robot_name` attribute to the decorated
            method of function.
        tags: Keyword tags. Sets `robot_tags` attribute.
        types: Argument types. Sets `robot_types` attribute.

            Value can be:

            - a dictionary mapping argument names to types,
            - a list of types mapped to arguments based on position, or
            - `None` to disable argument conversion altogether.

            It is OK to specify types only to some arguments. In normal usage
            it is recommended to specify types using type hints.

    If the automatic keyword discovery has been disabled with the
    [library][robot.api.deco.library] decorator or by setting the
    `ROBOT_AUTO_KEYWORDS` attribute to a false value, this decorator is
    needed to mark functions or methods keywords. In such usage this decorator
    is typically used without any arguments like `@keyword`.

    Examples:

        @keyword
        def example():
            ...

        @keyword('Login as user "${user}" with password "${password}"',
                 tags=['custom name', 'embedded arguments', 'tags'])
        def login(user, password):
            ...

        @keyword(types={'length': int, 'case_insensitive': bool})
        def types_as_dict(length, case_insensitive):
            ...

        @keyword(types=[int, bool])
        def types_as_list(length, case_insensitive):
            ...

        @keyword
        def types_using_type_hints(length: int, case_insensitive: bool):
            ...

        @keyword(types=None)
        def no_conversion(length, case_insensitive=False):
            ...
    """
    if callable(name):
        return keyword()(name)

    def decorator(func: F) -> F:
        func.robot_name = name
        func.robot_tags = tags
        func.robot_types = types
        return func

    return decorator


@overload
def library(cls: L, /) -> L:
    ...


@overload
def library(scope: 'Scope | None' = None,
            version: 'str | None' = None,
            converters: 'dict[type, Converter] | None' = None,
            doc_format: 'DocFormat | None' = None,
            listener: 'Any | None' = None,
            auto_keywords: bool = False) -> LibraryDecorator:
    ...


@not_keyword
def library(scope: 'L | Scope | None' = None,
            version: 'str | None' = None,
            converters: 'dict[type, Converter] | None' = None,
            doc_format: 'DocFormat | None' = None,
            listener: 'Any | None' = None,
            auto_keywords: bool = False) -> 'L | LibraryDecorator':
    """Class decorator to control keyword discovery and other library settings.

    Parameters:
        scope: Library scope.
            Sets class attribute `ROBOT_LIBRARY_SCOPE`.
        version: Library version.
            Sets class attribute `ROBOT_LIBRARY_VERSION`.
        converters: Custom argument converters.
            Sets class attribute `ROBOT_LIBRARY_CONVERTERS`.
        doc_format: Library documentation format.
            Sets class attribute `ROBOT_LIBRARY_DOC_FORMAT`.
        listener: Library listener or listeners.
            Sets class attribute `ROBOT_LIBRARY_LISTENER`.
        auto_keywords: Controls keyword discovery. When `False` (default), keywords
            need to be explicitly decorated with the [keyword][robot.api.deco.keyword]
            decorator. When `True`, all public methods become keywords.
            Sets class attribute `ROBOT_AUTO_KEYWORDS`.

    The `ROBOT_AUTO_KEYWORDS` class attribute is always set, but other class
    attributes are set only if parameters controlling them are used. All
    class attributes that are set override possible existing class attributes.

    This decorator can be used simply like `@library` to enable keyword discovery
    if there is no need to use any parameters.

    Examples:

        @library
        class KeywordDiscovery:

            @keyword
            def do_something(self):
                ...

            def not_keyword(self):
                ...


        @library(scope='GLOBAL', version='3.2', auto_keywords=True)
        class LibraryConfiguration:
            ...

    The `converters` argument is new in Robot Framework 5.0.
    """
    if isinstance(scope, type):
        return library()(scope)

    def decorator(cls: L) -> L:
        if scope is not None:
            cls.ROBOT_LIBRARY_SCOPE = scope
        if version is not None:
            cls.ROBOT_LIBRARY_VERSION = version
        if converters is not None:
            cls.ROBOT_LIBRARY_CONVERTERS = converters
        if doc_format is not None:
            cls.ROBOT_LIBRARY_DOC_FORMAT = doc_format
        if listener is not None:
            cls.ROBOT_LIBRARY_LISTENER = listener
        cls.ROBOT_AUTO_KEYWORDS = auto_keywords
        return cls

    return decorator
