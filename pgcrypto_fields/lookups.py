from django.db.models.lookups import Lookup

from pgcrypto_fields import aggregates


class HashLookup(Lookup):
    """Lookup to filter hashed values.

    `HashLookup` is hashing the value on the right hand side with
    the function specified in `encrypt_sql`.

    `lookup_name` is the lookup name appended to a field query.

    `encrypt_sql` is the pgcrypto to append to the field's value.
    """
    lookup_name = 'hash'
    encrypt_sql = aggregates.Digest.encrypt_sql

    def as_sql(self, qn, connection):
        """Responsible for creating the lookup with the digest SQL.

        Modify the right hand side expression to compare the value passed
        to a hash.
        """
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params

        rhs = self.encrypt_sql % rhs
        return '%s = %s' % (lhs, rhs), params
