# Flashcards API Endpoints

| Method   | URL                                     | Description                    |
| -------- | --------------------------------------- | ------------------------------ |
| `GET`    | [`/api/decks`](#get-decks)              | List all decks.                |
| `POST`   | [`/api/decks`](#add-deck)               | Create a new deck.             |
| `GET`    | [`/api/decks/10`](#get-deck)            | Retrieve deck #10.             |
| `PUT`    | [`/api/decks/10`](#update-deck)         | Update data in deck #10.       |
| `DELETE` | [`/api/decks/10`](#delete-deck)         | Delete deck #10.               |
| `GET`    | [`/api/decks/10/cards`](#get-cards)     | List all cards from deck #10.  |
| `POST`   | [`/api/decks/10/cards`](#add-card)      | Add card to deck #10.          |
| `GET`    | [`/api/decks/10/cards/2`](#get-card)    | Retrieve card #2.              |
| `PUT`    | [`/api/decks/10/cards/2`](#update-card) | Update data in card #2         |
| `DELETE` | [`/api/decks/10/cards/2`](#delete-card) | Delete card #2.                |
| `GET`    | [`/api/decks/10/boxes`](#get-boxes)     | List all boxes from deck #10.  |
| `GET`    | [`/api/decks/10/boxes/3`](#get-box)     | Retrieve box #3 from deck #10. |

## List all Decks <a name="get-decks"></a>

### Request

`GET /api/decks`

### Response

```json
[
	{
		"id": 1,
		"name": "foo",
		"box_amount": 5,
		"total_cards": 21
	},
	{
		"id": 2,
		"name": "bar",
		"box_amount": 4,
		"total_cards": 14
	}
]
```

## Create a new Deck <a name="add-deck"></a>

### Request

`POST /api/decks`

```json
{
	"name": "foo",
	"box_amount": 5
}
```

### Response

```json
{
	"message": "Deck successfully created"
}
```

## Retrieve a specific Deck <a name="get-deck"></a>

### Request

`GET /api/decks/id`

### Response

```json
{
	"id": 1,
	"name": "foo",
	"box_amount": 5,
	"total_cards": 21
}
```

## Update a Deck <a name="update-deck"></a>

### Request

`PUT /api/decks/id`

```json
{
	"name": "foo",
	"box_amount": 3
}
```

### Response

```json
{
	"message": "Deck successfully updated"
}
```

## Delete a Deck <a name="delete-deck"></a>

### Request

`DELETE /api/decks/id`

### Response

```json
{
	"message": "Deck successfully deleted"
}
```

## List all Cards <a name="get-cards"></a>

### Request

`GET /api/decks/id/cards`

### Response

```json
[
	{
		"id": 1,
		"front": "foo",
		"back": "bar"
	},
	{
		"id": 2,
		"front": "bar",
		"back": "baz"
	}
]
```

## Create a new Card <a name="add-card"></a>

### Request

`POST /api/decks/id/cards`

```json
{
	"front": "foo",
	"back": "bar"
}
```

### Response

```json
{
	"message": "Card successfully created"
}
```

## Retrieve a specific Card <a name="get-card"></a>

### Request

`GET /api/decks/id/cards/id`

### Response

```json
{
	"id": 1,
	"front": "foo",
	"back": "bar"
}
```

## Update a Card <a name="update-card"></a>

### Request

`PUT /api/decks/id/cards/id`

```json
{
	"front": "foo",
	"back": "bar"
}
```

### Response

```json
{
	"message": "Card successfully updated"
}
```

## Delete a Card <a name="delete-card"></a>

### Request

`DELETE /api/decks/id/cards/id`

### Response

```json
{
	"message": "Card successfully deleted"
}
```

## List all Boxes <a name="get-boxes"></a>

### Request

`GET /api/decks/id/boxes`

### Response

```json
[
	{
		"id": 1,
		"number_of": 1,
		"cards_amount": 22
	},
	{
		"id": 2,
		"number_of": 2,
		"cards_amount": 12
	}
]
```

## Retrieve a specific Box <a name="get-box"></a>

### Request

`GET /api/decks/id/boxes/id`

### Response

```json
{
	"id": 1,
	"number_of": 1,
	"cards_amount": 22
}
```
