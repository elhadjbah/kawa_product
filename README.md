# Kawai Produits

> Version 1.0.0

## Path Table

| Method | Path | Description |
| --- | --- | --- |
| GET | [/api/produits](#getapiproduits) | Get Produits |
| POST | [/api/produits](#postapiproduits) | Create Produit |
| GET | [/api/produits/{produit_id}](#getapiproduitsproduit_id) | Get Produit |
| PUT | [/api/produits/{produit_id}](#putapiproduitsproduit_id) | Update Produit |
| DELETE | [/api/produits/{produit_id}](#deleteapiproduitsproduit_id) | Delete Produit |

## Reference Table

| Name | Path | Description                                                                                  |
| --- | --- |----------------------------------------------------------------------------------------------|
| ProduitSchema | [#/components/schemas/ProduitSchema](#componentsschemasproduitschema) | Schéma de l'objet produit retourné en réponse              |
| ProduitCreate | [#/components/schemas/ProduitCreate](#componentsschemasproduitcreate) | Schéma de l'objet produit a envoyé pour la création        |
| ProduitUpdate | [#/components/schemas/ProduitUpdate](#componentsschemasproduitupdate) | Schéma de l'objet produit a envoyé pour la modification    |
| ApiKey | [#/components/securitySchemes/ApiKey](#componentssecurityschemesapikey) | Schéma de l'objet utilisé dans le header pour l'authentification |

## Path Details

***

### [GET]/api/produits

- Summary  
Get Produits

- Description  
Récupérer la liste des produits disponibles

#### Responses

- 200 OK

`application/json`

```ts
{
  id?: Partial(integer) & Partial(null)
  nom: string
  description: string
  prix: number
  stock: integer
}[]
```

***

### [POST]/api/produits

- Summary  
Create Produit

- Description  
Ajouter un nouveau produit à la liste de produits

- Security  
ApiKey  

#### RequestBody

- application/json

```ts
{
  nom: string
  description: string
  prix: number
  stock: integer
}
```

#### Responses

- 201 Created

`application/json`

```ts
{
  id?: Partial(integer) & Partial(null)
  nom: string
  description: string
  prix: number
  stock: integer
}
```

***

### [GET]/api/produits/{produit_id}

- Summary  
Get Produit

- Description  
Récupérer un produit spécifique à partir de son id

#### Responses

- 200 OK

`application/json`

```ts
{
  id?: Partial(integer) & Partial(null)
  nom: string
  description: string
  prix: number
  stock: integer
}
```

***

### [PUT]/api/produits/{produit_id}

- Summary  
Update Produit

- Description  
Mettre à jour un produit existant à partir de son id

- Security  
ApiKey  

#### RequestBody

- application/json

```ts
{
  nom?: Partial(string) & Partial(null)
  description?: Partial(string) & Partial(null)
  prix?: Partial(number) & Partial(null)
  stock?: Partial(integer) & Partial(null)
}
```

#### Responses

- 200 OK

`application/json`

```ts
{
  id?: Partial(integer) & Partial(null)
  nom: string
  description: string
  prix: number
  stock: integer
}
```

***

### [DELETE]/api/produits/{produit_id}

- Summary  
Delete Produit

- Description  
Supprimer définitivement un produit existant à partir de son id

- Security  
ApiKey  

#### Responses

- 200 OK

`application/json`

```ts
{
  "title": "Response",
  "type": "boolean"
}
```

## References

### #/components/schemas/ProduitSchema

```ts
{
  id?: Partial(integer) & Partial(null)
  nom: string
  description: string
  prix: number
  stock: integer
}
```

### #/components/schemas/ProduitCreate

```ts
{
  nom: string
  description: string
  prix: number
  stock: integer
}
```

### #/components/schemas/ProduitUpdate

```ts
{
  nom?: Partial(string) & Partial(null)
  description?: Partial(string) & Partial(null)
  prix?: Partial(number) & Partial(null)
  stock?: Partial(integer) & Partial(null)
}
```

### #/components/securitySchemes/ApiKey

```ts
{
  "type": "apiKey",
  "in": "header",
  "name": "x-access-token"
}
```
