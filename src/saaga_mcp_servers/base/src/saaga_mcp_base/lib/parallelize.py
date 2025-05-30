import asyncio
import functools
import inspect
from typing import Any, Callable, Coroutine, Dict, List, TypeVar, cast, get_type_hints

T = TypeVar("T", bound=Callable[..., Coroutine[Any, Any, Any]])


def _get_original_param_details(func: Callable) -> str:
    """Helper to format original parameter details for the docstring."""
    original_params_list = []
    try:
        sig = inspect.signature(func)
        # Attempt to use get_type_hints for more robust type information
        try:
            type_hints = get_type_hints(func)
        except Exception:  # Broad exception as get_type_hints can fail
            type_hints = {}

        for name, param in sig.parameters.items():
            annotation_display = "Any"  # Default if no annotation found
            if name in type_hints:
                hint = type_hints[name]
                # Try to get a readable name for the type hint
                if hasattr(hint, '_name') and hint._name is not None: # For typing._SpecialForm like List, Dict
                    annotation_str = str(hint)
                    annotation_display = annotation_str.replace('typing.', '')
                elif hasattr(hint, '__name__'): # For standard types like int, str
                    annotation_display = hint.__name__
                else: # Fallback for complex types
                    annotation_str = str(hint)
                    annotation_display = annotation_str.replace('typing.', '')
            elif param.annotation is not inspect.Parameter.empty:
                if hasattr(param.annotation, '__name__'):
                    annotation_display = param.annotation.__name__
                else:
                    annotation_str = str(param.annotation)
                    annotation_display = annotation_str.replace('typing.', '')
            
            original_params_list.append(f"            - `{name}: {annotation_display}`")
            
    except (ValueError, TypeError):  # Fallback if inspect.signature fails
        # This fallback might be less common with modern Python but good for robustness
        param_annotations = getattr(func, "__annotations__", {})
        for k, v_type in param_annotations.items():
            if k == "return":
                continue
            type_name = getattr(v_type, '__name__', str(v_type)).replace('typing.', '')
            original_params_list.append(f"            - `{k}: {type_name}`")

    if not original_params_list:
        return "        (Could not reliably determine original parameters or their types)"
    return "\n".join(original_params_list)


def _build_parallelized_docstring(func: Callable) -> str:
    """Constructs the docstring for the parallelized wrapper function."""
    original_doc = func.__doc__.strip() if func.__doc__ else "No original docstring provided."
    original_params_str = _get_original_param_details(func)
    func_name = func.__name__

    return f"""Parallelized version of `{func_name}`.

    This function accepts a list of keyword argument dictionaries and executes
    `{func_name}` concurrently for each set of arguments.

    Original docstring for `{func_name}`:
    {original_doc}

    Each dictionary in the `kwargs_list` should provide the keyword arguments
    expected by the original function (`{func_name}`). These are:
{original_params_str}

    Args:
        kwargs_list (List[Dict[str, Any]]): A list of dictionaries, where each
                                          dictionary provides the keyword arguments
                                          for a single call to `{func_name}`.

    Returns:
        List[Any]: A list containing the results of each call to `{func_name}`,
                   in the same order as the input `kwargs_list`.
    """

def _set_parallelized_signature_and_annotations(
    wrapper_func: Callable, 
    param_name: str, 
    param_annotation: Any, 
    return_annotation: Any
):
    """Sets the __signature__ and __annotations__ for the wrapper function."""
    new_param = inspect.Parameter(
        name=param_name,
        kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
        annotation=param_annotation
    )
    
    new_sig = inspect.Signature(
        parameters=[new_param],
        return_annotation=return_annotation
    )
    
    wrapper_func.__signature__ = new_sig
    wrapper_func.__annotations__ = {
        param_name: param_annotation,
        'return': return_annotation
    }


def parallelize(func: T) -> Callable[[List[Dict[str, Any]]], Coroutine[Any, Any, List[Any]]]:
    """
    Decorator to parallelize an async function.

    The decorated function will accept a list of keyword argument dictionaries.
    It will then run the original function concurrently for each set of kwargs
    using asyncio.gather and return a list of results.

    The docstring and signature of the decorated function will be updated to reflect
    this new calling convention.
    """

    @functools.wraps(func)
    async def wrapper(kwargs_list: List[Dict[str, Any]]) -> List[Any]:
        """
        Wrapper function that executes the original function in parallel.
        This docstring will be replaced by _build_parallelized_docstring.
        """
        if not isinstance(kwargs_list, list):
            raise TypeError(
                f"Input must be a list of dicts, got {type(kwargs_list)}"
            )
        if not all(isinstance(kwargs, dict) for kwargs in kwargs_list):
            raise TypeError("All items in kwargs_list must be dictionaries.")

        tasks = [func(**kwargs) for kwargs in kwargs_list]
        results = await asyncio.gather(*tasks)
        return results

    # Update the docstring and signature for the wrapper function
    wrapper.__doc__ = _build_parallelized_docstring(func)
    _set_parallelized_signature_and_annotations(
        wrapper_func=wrapper,
        param_name="kwargs_list",
        param_annotation=List[Dict[str, Any]],
        return_annotation=List[Any]
    )
    
    return cast(Callable[[List[Dict[str, Any]]], Coroutine[Any, Any, List[Any]]], wrapper)
