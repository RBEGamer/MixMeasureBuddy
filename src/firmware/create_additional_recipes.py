#!/usr/bin/env python3
"""Generate additional cocktail recipe files under src/recipes.

The script creates 50 common cocktail `.recipe` JSON files using a handful of
templated steps so they can be bundled later via the existing tooling.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List


REPO_ROOT = Path(__file__).resolve().parent.parent
RECIPES_DIR = REPO_ROOT / "recipes"


def step_scale(ingredient: str, amount: int, text: str = "") -> Dict[str, object]:
    return {
        "text": text,
        "ingredient": ingredient,
        "amount": int(amount),
        "action": 0,
    }


def step_confirm(text: str, ingredient: str = "", amount: int = -1) -> Dict[str, object]:
    return {
        "text": text,
        "ingredient": ingredient,
        "amount": int(amount),
        "action": 1,
    }


def step_wait(text: str, amount: int = -1) -> Dict[str, object]:
    return {
        "text": text,
        "ingredient": "",
        "amount": int(amount),
        "action": 2,
    }


COCKTAIL_SPECS: List[Dict[str, object]] = [
    {
        "name": "Bloody Mary",
        "description": "Savory brunch classic with vodka, tomato juice, citrus, and spice.",
        "method": "build",
        "ingredients": [
            step_scale("Vodka", 50),
            step_scale("Tomato Juice", 150),
            step_scale("Lemon Juice", 15),
            step_scale("Worcestershire Sauce", 5, "Add Worcestershire sauce"),
            step_scale("Hot Sauce", 2, "Add a few drops of hot sauce"),
            step_scale("Prepared Horseradish", 4, "Add prepared horseradish"),
        ],
        "post_steps": [step_wait("Season with salt and pepper to taste", -1)],
        "garnish": {
            "ingredient": "Celery Stick",
            "text": "Garnish with a celery stick and lemon wedge",
            "amount": 1,
        },
    },
    {
        "name": "Gin and Tonic",
        "description": "Crisp and bubbly highball of gin, tonic, and citrus.",
        "method": "build",
        "ingredients": [
            step_scale("Gin", 50),
            step_scale("Lime Juice", 10),
            step_scale("Tonic Water", 120, "Top with chilled tonic water"),
        ],
        "garnish": {
            "ingredient": "Lime Wedge",
            "text": "Garnish with a lime wedge",
            "amount": 1,
        },
    },
    {
        "name": "Moscow Mule",
        "description": "Vodka buck served icy cold with spicy ginger beer.",
        "method": "build",
        "ingredients": [
            step_scale("Vodka", 50),
            step_scale("Lime Juice", 15),
            step_scale("Ginger Beer", 120, "Top with fiery ginger beer"),
        ],
        "garnish": {
            "ingredient": "Lime Wheel",
            "text": "Garnish with a lime wheel",
            "amount": 1,
        },
    },
    {
        "name": "Rum and Coke",
        "description": "Simple and refreshing mix of rum, cola, and lime.",
        "method": "build",
        "ingredients": [
            step_scale("Aged Rum", 50),
            step_scale("Lime Juice", 10),
            step_scale("Cola", 150, "Top with chilled cola"),
        ],
        "garnish": {
            "ingredient": "Lime Wedge",
            "text": "Garnish with a lime wedge",
            "amount": 1,
        },
    },
    {
        "name": "Paloma",
        "description": "Bright tequila highball with grapefruit, lime, and sparkle.",
        "method": "build",
        "ingredients": [
            step_scale("Tequila", 50),
            step_scale("Grapefruit Juice", 90),
            step_scale("Lime Juice", 15),
            step_scale("Agave Syrup", 10, "Sweeten with agave syrup"),
            step_scale("Soda Water", 90, "Top with soda water"),
        ],
        "garnish": {
            "ingredient": "Grapefruit Wedge",
            "text": "Garnish with a grapefruit wedge",
            "amount": 1,
        },
    },
    {
        "name": "Tom Collins",
        "description": "Classic sparkling gin cooler with citrus and a touch of sweetness.",
        "method": "shake",
        "ingredients": [
            step_scale("Gin", 60),
            step_scale("Lemon Juice", 30),
            step_scale("Simple Syrup", 20),
        ],
        "post_steps": [step_scale("Soda Water", 90, "Top with soda water")],
        "garnish": {
            "ingredient": "Lemon Wheel",
            "text": "Garnish with a lemon wheel and cherry",
            "amount": 1,
        },
    },
    {
        "name": "Sidecar",
        "description": "Cognac sour accented with orange liqueur and citrus.",
        "method": "shake",
        "ingredients": [
            step_scale("Cognac", 50),
            step_scale("Triple Sec", 20),
            step_scale("Lemon Juice", 20),
        ],
        "garnish": {
            "ingredient": "Orange Twist",
            "text": "Garnish with an orange twist",
            "amount": 1,
        },
    },
    {
        "name": "French 75",
        "description": "Sparkling combination of gin, lemon, and Champagne.",
        "method": "shake",
        "ingredients": [
            step_scale("Gin", 40),
            step_scale("Lemon Juice", 15),
            step_scale("Simple Syrup", 15),
        ],
        "post_steps": [step_scale("Champagne", 90, "Top with chilled Champagne")],
        "garnish": {
            "ingredient": "Lemon Twist",
            "text": "Garnish with a lemon twist",
            "amount": 1,
        },
    },
    {
        "name": "Sazerac",
        "description": "Historic New Orleans cocktail built on rye, bitters, and absinthe aroma.",
        "method": "stir",
        "pre_steps": [step_confirm("Rinse a chilled glass with absinthe and discard the excess", "Absinthe", -1)],
        "ingredients": [
            step_scale("Rye Whiskey", 60),
            step_scale("Simple Syrup", 10),
            step_scale("Peychaud's Bitters", 2, "Add dashes of Peychaud's bitters"),
        ],
        "garnish": {
            "ingredient": "Lemon Peel",
            "text": "Express a lemon peel over the drink and discard",
            "amount": 1,
        },
    },
    {
        "name": "Mint Julep",
        "description": "Icy bourbon refresher with crushed mint and gentle sweetness.",
        "method": "build",
        "ingredients": [
            step_scale("Mint Leaves", 6, "Add fresh mint leaves"),
            step_scale("Simple Syrup", 20),
            step_scale("Bourbon", 60),
        ],
        "post_steps": [step_wait("Stir until the cup frosts", 20)],
        "garnish": {
            "ingredient": "Mint Sprig",
            "text": "Garnish with a bouquet of mint",
            "amount": 1,
        },
    },
    {
        "name": "Ramos Gin Fizz",
        "description": "Rich, frothy gin fizz with cream, citrus, and orange blossom.",
        "method": "shake",
        "ingredients": [
            step_scale("Gin", 45),
            step_scale("Lemon Juice", 15),
            step_scale("Lime Juice", 15),
            step_scale("Simple Syrup", 20),
            step_scale("Heavy Cream", 30),
            step_scale("Egg White", 1, "Add egg white"),
            step_scale("Orange Flower Water", 2, "Add orange flower water"),
        ],
        "post_steps": [step_scale("Soda Water", 90, "Top slowly with soda water")],
    },
    {
        "name": "Dark and Stormy",
        "description": "Dark rum highball balanced with lime and fiery ginger beer.",
        "method": "build",
        "ingredients": [
            step_scale("Dark Rum", 50),
            step_scale("Lime Juice", 15),
            step_scale("Ginger Beer", 120, "Top with ginger beer"),
        ],
        "garnish": {
            "ingredient": "Lime Wedge",
            "text": "Garnish with a lime wedge",
            "amount": 1,
        },
    },
    {
        "name": "Aviation",
        "description": "Classic gin sour tinted with maraschino and violet liqueur.",
        "method": "shake",
        "ingredients": [
            step_scale("Gin", 50),
            step_scale("Maraschino Liqueur", 15),
            step_scale("Crème de Violette", 10),
            step_scale("Lemon Juice", 20),
        ],
        "garnish": {
            "ingredient": "Brandied Cherry",
            "text": "Garnish with a brandied cherry",
            "amount": 1,
        },
    },
    {
        "name": "Corpse Reviver No 2",
        "description": "Equal-parts gin classic brightened with citrus and absinthe.",
        "method": "shake",
        "ingredients": [
            step_scale("Gin", 30),
            step_scale("Cointreau", 30),
            step_scale("Lillet Blanc", 30),
            step_scale("Lemon Juice", 30),
            step_scale("Absinthe", 2, "Add a dash of absinthe"),
        ],
        "garnish": {
            "ingredient": "Orange Peel",
            "text": "Garnish with an orange peel",
            "amount": 1,
        },
    },
    {
        "name": "Last Word",
        "description": "Prohibition-era equal-parts mix of gin, chartreuse, cherry, and lime.",
        "method": "shake",
        "ingredients": [
            step_scale("Gin", 25),
            step_scale("Green Chartreuse", 25),
            step_scale("Maraschino Liqueur", 25),
            step_scale("Lime Juice", 25),
        ],
        "garnish": {
            "ingredient": "Brandied Cherry",
            "text": "Garnish with a brandied cherry",
            "amount": 1,
        },
    },
    {
        "name": "Boulevardier",
        "description": "Bourbon's answer to the Negroni with bittersweet balance.",
        "method": "stir",
        "ingredients": [
            step_scale("Bourbon", 45),
            step_scale("Sweet Vermouth", 30),
            step_scale("Campari", 30),
        ],
        "garnish": {
            "ingredient": "Orange Twist",
            "text": "Garnish with an expressed orange twist",
            "amount": 1,
        },
    },
    {
        "name": "Bee's Knees",
        "description": "Roaring twenties gin sour sweetened solely with honey.",
        "method": "shake",
        "ingredients": [
            step_scale("Gin", 60),
            step_scale("Lemon Juice", 25),
            step_scale("Honey Syrup", 25),
        ],
        "garnish": {
            "ingredient": "Lemon Twist",
            "text": "Garnish with a lemon twist",
            "amount": 1,
        },
    },
    {
        "name": "Caipirinha",
        "description": "Brazil's national cocktail muddling lime, sugar, and cachaça.",
        "method": "build",
        "pre_steps": [step_confirm("Muddle lime wedges with sugar in the glass", "Lime Wedges", -1)],
        "ingredients": [
            step_scale("Demerara Sugar", 12),
            step_scale("Cachaça", 60),
        ],
        "garnish": {
            "ingredient": "Lime Wheel",
            "text": "Garnish with a lime wheel",
            "amount": 1,
        },
    },
    {
        "name": "Pisco Sour",
        "description": "Silky Peruvian sour with pisco, citrus, and a foam cap.",
        "method": "shake",
        "ingredients": [
            step_scale("Pisco", 60),
            step_scale("Lime Juice", 30),
            step_scale("Simple Syrup", 20),
            step_scale("Egg White", 1, "Add egg white"),
        ],
        "post_steps": [step_scale("Angostura Bitters", 3, "Dot bitters on top of the foam")],
    },
    {
        "name": "Bramble",
        "description": "Modern classic with gin, citrus, and blackberry liqueur.",
        "method": "shake",
        "ingredients": [
            step_scale("Gin", 50),
            step_scale("Lemon Juice", 25),
            step_scale("Simple Syrup", 15),
        ],
        "post_steps": [step_scale("Crème de Mûre", 15, "Drizzle blackberry liqueur over ice")],
        "garnish": {
            "ingredient": "Blackberry",
            "text": "Garnish with fresh blackberries",
            "amount": 2,
        },
    },
    {
        "name": "Clover Club",
        "description": "Pre-Prohibition raspberry gin sour finished with silky foam.",
        "method": "shake",
        "ingredients": [
            step_scale("Gin", 45),
            step_scale("Raspberry Syrup", 20),
            step_scale("Lemon Juice", 25),
            step_scale("Egg White", 1, "Add egg white"),
        ],
        "garnish": {
            "ingredient": "Raspberries",
            "text": "Garnish with fresh raspberries",
            "amount": 3,
        },
    },
    {
        "name": "Vesper Martini",
        "description": "Bond's blend of gin, vodka, and aromatized wine served icy cold.",
        "method": "stir",
        "ingredients": [
            step_scale("Gin", 60),
            step_scale("Vodka", 15),
            step_scale("Lillet Blanc", 15),
        ],
        "garnish": {
            "ingredient": "Lemon Peel",
            "text": "Garnish with a wide lemon peel",
            "amount": 1,
        },
    },
    {
        "name": "Paper Plane",
        "description": "Equal-parts modern sour with bourbon, Aperol, and amaro.",
        "method": "shake",
        "ingredients": [
            step_scale("Bourbon", 30),
            step_scale("Aperol", 30),
            step_scale("Amaro Nonino", 30),
            step_scale("Lemon Juice", 30),
        ],
        "garnish": {
            "ingredient": "Lemon Twist",
            "text": "Garnish with a lemon twist",
            "amount": 1,
        },
    },
    {
        "name": "Penicillin",
        "description": "Modern Scotch sour with honey, ginger, and smoky float.",
        "method": "shake",
        "ingredients": [
            step_scale("Blended Scotch", 45),
            step_scale("Lemon Juice", 20),
            step_scale("Honey-Ginger Syrup", 25),
        ],
        "post_steps": [step_scale("Islay Scotch", 10, "Float smoky Scotch on top")],
        "garnish": {
            "ingredient": "Candied Ginger",
            "text": "Garnish with candied ginger",
            "amount": 1,
        },
    },
    {
        "name": "El Diablo",
        "description": "Tequila highball with cassis, lime, and spicy ginger beer.",
        "method": "build",
        "ingredients": [
            step_scale("Tequila", 45),
            step_scale("Crème de Cassis", 20),
            step_scale("Lime Juice", 15),
            step_scale("Ginger Beer", 90, "Top with ginger beer"),
        ],
        "garnish": {
            "ingredient": "Lime Wheel",
            "text": "Garnish with a lime wheel",
            "amount": 1,
        },
    },
    {
        "name": "Jungle Bird",
        "description": "Tropical bitter-sweet mix of rum, Campari, and pineapple.",
        "method": "shake",
        "ingredients": [
            step_scale("Dark Rum", 45),
            step_scale("Campari", 30),
            step_scale("Pineapple Juice", 45),
            step_scale("Lime Juice", 15),
            step_scale("Demerara Syrup", 15),
        ],
        "garnish": {
            "ingredient": "Pineapple Leaf",
            "text": "Garnish with pineapple fronds",
            "amount": 1,
        },
    },
    {
        "name": "White Russian",
        "description": "Creamy dessert sipper with vodka and coffee liqueur.",
        "method": "build",
        "ingredients": [
            step_scale("Vodka", 45),
            step_scale("Coffee Liqueur", 30),
            step_scale("Heavy Cream", 30, "Float cream over the back of a spoon"),
        ],
    },
    {
        "name": "Black Russian",
        "description": "Simple blend of vodka and coffee liqueur served over ice.",
        "method": "build",
        "ingredients": [
            step_scale("Vodka", 50),
            step_scale("Coffee Liqueur", 25),
        ],
    },
    {
        "name": "Irish Coffee",
        "description": "Warming mug of Irish whiskey, coffee, and lightly whipped cream.",
        "method": "hot",
        "skip_prepare": True,
        "pre_steps": [step_confirm("Preheat the glass with hot water", "", -1)],
        "ingredients": [
            step_scale("Irish Whiskey", 40),
            step_scale("Brown Sugar Syrup", 15),
            step_scale("Hot Coffee", 150),
        ],
        "post_steps": [step_scale("Lightly Whipped Cream", 30, "Float cream on top")],
        "garnish": {
            "ingredient": "Grated Nutmeg",
            "text": "Dust lightly with grated nutmeg",
            "amount": 1,
        },
    },
    {
        "name": "Hot Toddy",
        "description": "Comforting mix of whiskey, honey, lemon, and hot water.",
        "method": "hot",
        "skip_prepare": True,
        "pre_steps": [step_confirm("Warm the mug before building the drink", "", -1)],
        "ingredients": [
            step_scale("Irish Whiskey", 45),
            step_scale("Honey Syrup", 20),
            step_scale("Lemon Juice", 20),
            step_scale("Hot Water", 120),
        ],
        "garnish": {
            "ingredient": "Lemon Wheel",
            "text": "Garnish with a lemon wheel and clove",
            "amount": 1,
        },
    },
    {
        "name": "Whiskey Smash",
        "description": "Minty bourbon sour with fresh lemon and crushed ice.",
        "method": "shake",
        "pre_steps": [step_confirm("Muddle lemon wedges and mint in the shaker", "Mint Leaves", -1)],
        "ingredients": [
            step_scale("Bourbon", 60),
            step_scale("Simple Syrup", 20),
            step_scale("Mint Leaves", 6),
        ],
        "garnish": {
            "ingredient": "Mint Sprig",
            "text": "Garnish with a fresh mint sprig",
            "amount": 1,
        },
    },
    {
        "name": "Old Cuban",
        "description": "Sparkling aged rum cocktail with mint and aromatic bitters.",
        "method": "shake",
        "ingredients": [
            step_scale("Aged Rum", 45),
            step_scale("Lime Juice", 20),
            step_scale("Simple Syrup", 20),
            step_scale("Mint Leaves", 6),
            step_scale("Angostura Bitters", 2, "Add dashes of bitters"),
        ],
        "post_steps": [step_scale("Sparkling Wine", 90, "Top with sparkling wine")],
        "garnish": {
            "ingredient": "Mint Sprig",
            "text": "Garnish with an elegant mint sprig",
            "amount": 1,
        },
    },
    {
        "name": "Southside",
        "description": "Herbaceous gin sour shaken with mint and lime.",
        "method": "shake",
        "ingredients": [
            step_scale("Gin", 60),
            step_scale("Lime Juice", 25),
            step_scale("Simple Syrup", 20),
            step_scale("Mint Leaves", 6),
        ],
        "garnish": {
            "ingredient": "Mint Sprig",
            "text": "Garnish with a mint sprig",
            "amount": 1,
        },
    },
    {
        "name": "Palmetto",
        "description": "Rum-based Manhattan featuring sweet vermouth and orange bitters.",
        "method": "stir",
        "ingredients": [
            step_scale("Aged Rum", 50),
            step_scale("Sweet Vermouth", 30),
            step_scale("Orange Bitters", 2, "Add dashes of orange bitters"),
        ],
        "garnish": {
            "ingredient": "Orange Twist",
            "text": "Garnish with an orange twist",
            "amount": 1,
        },
    },
    {
        "name": "Tequila Sunrise",
        "description": "Layered tequila cocktail with orange juice and grenadine sunrise.",
        "method": "build",
        "skip_mix_step": True,
        "ingredients": [
            step_scale("Tequila", 45),
            step_scale("Orange Juice", 120),
            step_scale("Grenadine", 15, "Slowly pour grenadine to sink"),
        ],
        "garnish": {
            "ingredient": "Orange Slice",
            "text": "Garnish with an orange slice and cherry",
            "amount": 1,
        },
    },
    {
        "name": "Sea Breeze",
        "description": "Vodka highball with cranberry bite and grapefruit zest.",
        "method": "build",
        "ingredients": [
            step_scale("Vodka", 50),
            step_scale("Cranberry Juice", 90),
            step_scale("Grapefruit Juice", 60),
        ],
        "garnish": {
            "ingredient": "Lime Wedge",
            "text": "Garnish with a lime wedge",
            "amount": 1,
        },
    },
    {
        "name": "Bay Breeze",
        "description": "Tropical cranberry cooler with pineapple sweetness.",
        "method": "build",
        "ingredients": [
            step_scale("Vodka", 50),
            step_scale("Cranberry Juice", 90),
            step_scale("Pineapple Juice", 60),
        ],
        "garnish": {
            "ingredient": "Pineapple Wedge",
            "text": "Garnish with a pineapple wedge",
            "amount": 1,
        },
    },
    {
        "name": "Sex on the Beach",
        "description": "Fruity crowd-pleaser with vodka, peach, and citrus juices.",
        "method": "build",
        "ingredients": [
            step_scale("Vodka", 45),
            step_scale("Peach Schnapps", 30),
            step_scale("Cranberry Juice", 90),
            step_scale("Orange Juice", 90),
        ],
        "garnish": {
            "ingredient": "Orange Slice",
            "text": "Garnish with an orange slice and cherry",
            "amount": 1,
        },
    },
    {
        "name": "Long Island Iced Tea",
        "description": "High-octane highball combining mixed white spirits, citrus, and cola.",
        "method": "shake",
        "ingredients": [
            step_scale("Vodka", 15),
            step_scale("Gin", 15),
            step_scale("White Rum", 15),
            step_scale("Blanco Tequila", 15),
            step_scale("Triple Sec", 15),
            step_scale("Lemon Juice", 25),
            step_scale("Simple Syrup", 20),
        ],
        "post_steps": [step_scale("Cola", 90, "Top with cola")],
        "garnish": {
            "ingredient": "Lemon Wheel",
            "text": "Garnish with a lemon wheel",
            "amount": 1,
        },
    },
    {
        "name": "Hurricane",
        "description": "Passion fruit-forward rum punch from New Orleans.",
        "method": "shake",
        "ingredients": [
            step_scale("Light Rum", 45),
            step_scale("Dark Rum", 45),
            step_scale("Passion Fruit Syrup", 30),
            step_scale("Orange Juice", 45),
            step_scale("Lime Juice", 15),
            step_scale("Grenadine", 15),
        ],
        "garnish": {
            "ingredient": "Orange Slice",
            "text": "Garnish with an orange slice and cherry",
            "amount": 1,
        },
    },
    {
        "name": "Planter's Punch",
        "description": "Classic Jamaican rum punch with citrus and spice.",
        "method": "shake",
        "ingredients": [
            step_scale("Dark Rum", 60),
            step_scale("Lime Juice", 25),
            step_scale("Grenadine", 15),
            step_scale("Simple Syrup", 15),
            step_scale("Angostura Bitters", 2, "Add dashes of bitters"),
        ],
        "garnish": {
            "ingredient": "Orange Wheel",
            "text": "Garnish with an orange wheel and cherry",
            "amount": 1,
        },
    },
    {
        "name": "Singapore Sling",
        "description": "Layered gin sling with cherry, citrus, and sparkling length.",
        "method": "shake",
        "ingredients": [
            step_scale("Gin", 30),
            step_scale("Cherry Heering", 20),
            step_scale("Cointreau", 10),
            step_scale("Bénédictine", 10),
            step_scale("Pineapple Juice", 90),
            step_scale("Lime Juice", 15),
            step_scale("Grenadine", 10),
        ],
        "post_steps": [step_scale("Soda Water", 60, "Top with soda water")],
        "garnish": {
            "ingredient": "Pineapple Wedge",
            "text": "Garnish with pineapple and cherry",
            "amount": 1,
        },
    },
    {
        "name": "Bahama Mama",
        "description": "Vacation-ready rum medley with pineapple, orange, and coffee notes.",
        "method": "shake",
        "ingredients": [
            step_scale("Dark Rum", 30),
            step_scale("Coconut Rum", 30),
            step_scale("Coffee Liqueur", 15),
            step_scale("Pineapple Juice", 90),
            step_scale("Orange Juice", 60),
            step_scale("Lemon Juice", 15),
        ],
        "garnish": {
            "ingredient": "Pineapple Slice",
            "text": "Garnish with pineapple and cherry",
            "amount": 1,
        },
    },
    {
        "name": "Painkiller",
        "description": "Creamy tiki staple with rum, pineapple, orange, and coconut.",
        "method": "blend",
        "ingredients": [
            step_scale("Navy Rum", 60),
            step_scale("Pineapple Juice", 120),
            step_scale("Orange Juice", 30),
            step_scale("Cream of Coconut", 30),
        ],
        "garnish": {
            "ingredient": "Grated Nutmeg",
            "text": "Dust the top with freshly grated nutmeg",
            "amount": 1,
        },
    },
    {
        "name": "Zombie",
        "description": "Potent tiki mix of rums, citrus, spice, and tropical sweetness.",
        "method": "shake",
        "ingredients": [
            step_scale("Light Rum", 30),
            step_scale("Dark Rum", 30),
            step_scale("Overproof Rum", 15),
            step_scale("Lime Juice", 20),
            step_scale("Grapefruit Juice", 30),
            step_scale("Cinnamon Syrup", 15),
            step_scale("Grenadine", 10),
            step_scale("Falernum", 10),
        ],
        "garnish": {
            "ingredient": "Mint Sprig",
            "text": "Garnish with mint and a spent lime shell",
            "amount": 1,
        },
    },
    {
        "name": "Mezcal Paloma",
        "description": "Smoky variation on the Paloma with mezcal and grapefruit.",
        "method": "build",
        "ingredients": [
            step_scale("Mezcal", 50),
            step_scale("Grapefruit Juice", 90),
            step_scale("Lime Juice", 15),
            step_scale("Agave Syrup", 10),
            step_scale("Soda Water", 90, "Top with soda water"),
        ],
        "garnish": {
            "ingredient": "Grapefruit Wedge",
            "text": "Garnish with a grapefruit wedge",
            "amount": 1,
        },
    },
    {
        "name": "Gin Basil Smash",
        "description": "Vibrant gin sour infused with muddled basil and lemon.",
        "method": "shake",
        "pre_steps": [step_confirm("Muddle basil leaves with lemon juice in the shaker", "Basil Leaves", -1)],
        "ingredients": [
            step_scale("Gin", 60),
            step_scale("Lemon Juice", 25),
            step_scale("Simple Syrup", 20),
            step_scale("Basil Leaves", 8),
        ],
        "garnish": {
            "ingredient": "Basil Leaf",
            "text": "Garnish with a basil leaf",
            "amount": 1,
        },
    },
    {
        "name": "Rosemary Greyhound",
        "description": "Botanical vodka highball with grapefruit and rosemary.",
        "method": "build",
        "pre_steps": [step_confirm("Lightly muddle rosemary in the glass", "Rosemary Sprig", -1)],
        "ingredients": [
            step_scale("Vodka", 50),
            step_scale("Grapefruit Juice", 120),
            step_scale("Simple Syrup", 15),
        ],
        "garnish": {
            "ingredient": "Rosemary Sprig",
            "text": "Garnish with a rosemary sprig",
            "amount": 1,
        },
    },
    {
        "name": "Blood and Sand",
        "description": "Scotch classic marrying citrus, cherry, and sweet vermouth.",
        "method": "shake",
        "ingredients": [
            step_scale("Scotch Whisky", 30),
            step_scale("Sweet Vermouth", 30),
            step_scale("Cherry Liqueur", 30),
            step_scale("Orange Juice", 30),
        ],
        "garnish": {
            "ingredient": "Orange Peel",
            "text": "Garnish with an orange peel",
            "amount": 1,
        },
    },
    {
        "name": "Brooklyn",
        "description": "Rye Manhattan variation with dry vermouth and bittersweet notes.",
        "method": "stir",
        "ingredients": [
            step_scale("Rye Whiskey", 50),
            step_scale("Dry Vermouth", 20),
            step_scale("Maraschino Liqueur", 5),
            step_scale("Amaro", 10),
        ],
        "garnish": {
            "ingredient": "Brandied Cherry",
            "text": "Garnish with a brandied cherry",
            "amount": 1,
        },
    },
]


def sanitize_filename(name: str) -> str:
    filename = re.sub(r"[^0-9a-zA-Z]+", "_", name)
    filename = filename.strip("_")
    if not filename:
        filename = "RECIPE"
    if filename[0].isdigit():
        filename = f"RECIPE_{filename}"
    return filename


def build_steps(spec: Dict[str, object]) -> List[Dict[str, object]]:
    steps: List[Dict[str, object]] = []
    steps.extend(spec.get("pre_steps", []))  # type: ignore[arg-type]

    method = str(spec.get("method", "shake")).lower()
    prepare_step = {
        "shake": step_confirm("Add ice to the shaker", "Ice"),
        "stir": step_confirm("Add ice to the mixing glass", "Ice"),
        "build": step_confirm("Fill the serving glass with ice", "Ice"),
        "blend": step_confirm("Add crushed ice to the blender", "Ice"),
        "hot": step_confirm("Prepare the warm mug", "", -1),
    }.get(method)

    if prepare_step and not spec.get("skip_prepare"):
        steps.append(prepare_step)

    for ingredient_step in spec["ingredients"]:  # type: ignore[assignment]
        steps.append(ingredient_step)

    if method == "shake":
        steps.append(step_wait("Shake until well chilled", 15))
        steps.append(step_wait("Strain into a prepared glass", -1))
    elif method == "stir":
        steps.append(step_wait("Stir until well chilled", 20))
        steps.append(step_wait("Strain into a chilled glass", -1))
    elif method == "build" and not spec.get("skip_mix_step"):
        steps.append(step_wait("Stir gently to combine", 10))
    elif method == "blend":
        steps.append(step_wait("Blend until smooth", 20))
        steps.append(step_wait("Pour into the serving glass", -1))
    elif method == "hot":
        steps.append(step_wait("Stir to combine and integrate flavors", 15))

    steps.extend(spec.get("post_steps", []))  # type: ignore[arg-type]

    garnish: Dict[str, object] | None = spec.get("garnish")  # type: ignore[assignment]
    if garnish:
        garnish_amount = int(garnish.get("amount", 1))
        garnish_text = str(garnish.get("text", "Add garnish"))
        garnish_ingredient = str(garnish.get("ingredient", "Garnish"))
        steps.append(step_confirm(garnish_text, garnish_ingredient, garnish_amount))

    return steps


def write_recipe(spec: Dict[str, object]) -> None:
    filename_base = sanitize_filename(str(spec["name"]))
    filename = f"{filename_base}.recipe"
    output_path = RECIPES_DIR / filename

    steps = build_steps(spec)

    recipe_doc = {
        "filename": filename,
        "name": spec["name"],
        "steps": steps,
        "description": spec["description"],
        "version": "1.0.0",
    }

    output_path.write_text(json.dumps(recipe_doc, indent=4), encoding="utf-8")
    print(f"Wrote {output_path.relative_to(REPO_ROOT)}")


def main() -> None:
    RECIPES_DIR.mkdir(parents=True, exist_ok=True)
    for spec in COCKTAIL_SPECS:
        write_recipe(spec)


if __name__ == "__main__":
    main()
