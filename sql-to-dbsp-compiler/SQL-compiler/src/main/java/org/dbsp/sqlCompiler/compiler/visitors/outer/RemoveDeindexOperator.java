package org.dbsp.sqlCompiler.compiler.visitors.outer;

import org.dbsp.sqlCompiler.circuit.operator.*;
import org.dbsp.sqlCompiler.compiler.IErrorReporter;

/**
 * Convert Deindex operators into simple Map operators.
 */
public class RemoveDeindexOperator extends CircuitCloneVisitor {
    public RemoveDeindexOperator(IErrorReporter reporter) {
        super(reporter, false);
    }

    @Override
    public void postorder(DBSPDeindexOperator operator) {
        DBSPOperator input = this.mapped(operator.input());
        DBSPMapOperator result = new DBSPMapOperator(operator.getNode(), operator.getFunction(),
                operator.getType(), input);
        this.map(operator, result);
    }
}
