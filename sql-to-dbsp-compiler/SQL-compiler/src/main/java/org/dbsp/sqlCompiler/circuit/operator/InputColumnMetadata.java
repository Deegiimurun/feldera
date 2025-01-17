package org.dbsp.sqlCompiler.circuit.operator;

import org.dbsp.sqlCompiler.ir.expression.DBSPExpression;
import org.dbsp.sqlCompiler.ir.type.DBSPType;

import javax.annotation.Nullable;

/**
 * Metadata describing an input table column.
 */
public class InputColumnMetadata {
    /**
     * Column name.
     */
    public final String name;
    /**
     * Column type.
     */
    public final DBSPType type;
    /**
     * True if the column is a primary key.
     */
    public final boolean isPrimaryKey;
    /**
     * Lateness, if declared.  Should be a constant expression.
     */
    @Nullable
    public final DBSPExpression lateness;

    public InputColumnMetadata(String name, DBSPType type, boolean isPrimaryKey,
                               @Nullable DBSPExpression lateness) {
        this.name = name;
        this.type = type;
        this.isPrimaryKey = isPrimaryKey;
        this.lateness = lateness;
    }

    public String getName() {
        return this.name;
    }

    public DBSPType getType() {
        return this.type;
    }
}
