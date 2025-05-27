"""Chains package for GM sender."""
from .megaETH import MegaETHChain
from .unichain import Unichain
from .soneium import Soneium
from .inkchain import Inkchain
from .monad import Monad

# Dictionary of available chains
AVAILABLE_CHAINS = {
    "megaeth": MegaETHChain,
    "unichain": Unichain,
    "soneium": Soneium,
    "inkchain": Inkchain,
    "monad": Monad,
}

def get_chain(chain_name):
    """Get a chain by name.
    
    Args:
        chain_name: Name of the chain to get (case insensitive)
        
    Returns:
        Chain class or None if not found
    """
    return AVAILABLE_CHAINS.get(chain_name.lower()) 