/* High-performance physics and collision detection module for game.py
 * Compile with: python setup.py build_ext --inplace
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <math.h>
#include <stdbool.h>

/* Vector2 structure for efficient calculations */
typedef struct {
    double x, y;
} Vector2;

/* Rect structure matching pygame.Rect */
typedef struct {
    int x, y, w, h;
} Rect;

/* Helper: Normalize a vector */
static void normalize_vector(Vector2 *v) {
    double len = sqrt(v->x * v->x + v->y * v->y);
    if (len > 0.0001) {
        v->x /= len;
        v->y /= len;
    }
}

/* Helper: Calculate vector from point A to point B (normalized) */
static Vector2 vec_toward_internal(double ax, double ay, double bx, double by) {
    Vector2 result;
    result.x = bx - ax;
    result.y = by - ay;
    normalize_vector(&result);
    return result;
}

/* Fast rect-rect collision detection */
static bool rect_collide(const Rect *a, const Rect *b) {
    return !(a->x + a->w < b->x || b->x + b->w < a->x ||
             a->y + a->h < b->y || b->y + b->h < a->y);
}

/* Check if a rect can move without colliding with a list of rects */
static PyObject* can_move_rect_c(PyObject* self, PyObject* args) {
    int rect_x, rect_y, rect_w, rect_h, dx, dy;
    PyObject* other_rects_list;
    int screen_width, screen_height;
    
    if (!PyArg_ParseTuple(args, "iiiiiiOii", 
                          &rect_x, &rect_y, &rect_w, &rect_h,
                          &dx, &dy, &other_rects_list,
                          &screen_width, &screen_height)) {
        return NULL;
    }
    
    // Test rect after movement
    Rect test_rect;
    test_rect.x = rect_x + dx;
    test_rect.y = rect_y + dy;
    test_rect.w = rect_w;
    test_rect.h = rect_h;
    
    // Check screen bounds
    if (test_rect.x < 0 || test_rect.x + test_rect.w > screen_width ||
        test_rect.y < 0 || test_rect.y + test_rect.h > screen_height) {
        Py_RETURN_FALSE;
    }
    
    // Check collisions with other rects
    Py_ssize_t len = PyList_Size(other_rects_list);
    for (Py_ssize_t i = 0; i < len; i++) {
        PyObject* other_rect = PyList_GetItem(other_rects_list, i);
        if (!other_rect) continue;
        
        // Extract rect attributes (assuming pygame.Rect object)
        PyObject* x_attr = PyObject_GetAttrString(other_rect, "x");
        PyObject* y_attr = PyObject_GetAttrString(other_rect, "y");
        PyObject* w_attr = PyObject_GetAttrString(other_rect, "w");
        PyObject* h_attr = PyObject_GetAttrString(other_rect, "h");
        
        if (!x_attr || !y_attr || !w_attr || !h_attr) {
            Py_XDECREF(x_attr);
            Py_XDECREF(y_attr);
            Py_XDECREF(w_attr);
            Py_XDECREF(h_attr);
            continue;
        }
        
        Rect other;
        other.x = (int)PyLong_AsLong(x_attr);
        other.y = (int)PyLong_AsLong(y_attr);
        other.w = (int)PyLong_AsLong(w_attr);
        other.h = (int)PyLong_AsLong(h_attr);
        
        Py_DECREF(x_attr);
        Py_DECREF(y_attr);
        Py_DECREF(w_attr);
        Py_DECREF(h_attr);
        
        if (rect_collide(&test_rect, &other)) {
            Py_RETURN_FALSE;
        }
    }
    
    Py_RETURN_TRUE;
}

/* Fast vector toward calculation */
static PyObject* vec_toward_c(PyObject* self, PyObject* args) {
    double ax, ay, bx, by;
    
    if (!PyArg_ParseTuple(args, "dddd", &ax, &ay, &bx, &by)) {
        return NULL;
    }
    
    Vector2 v = vec_toward_internal(ax, ay, bx, by);
    
    // Return as tuple (x, y)
    return Py_BuildValue("(dd)", v.x, v.y);
}

/* Batch update bullet positions */
static PyObject* update_bullets_c(PyObject* self, PyObject* args) {
    PyObject* bullets_list;
    double dt;
    int screen_width, screen_height;
    
    if (!PyArg_ParseTuple(args, "Odii", &bullets_list, &dt, 
                          &screen_width, &screen_height)) {
        return NULL;
    }
    
    Py_ssize_t len = PyList_Size(bullets_list);
    PyObject* result = PyList_New(0);
    if (!result) return NULL;
    
    for (Py_ssize_t i = 0; i < len; i++) {
        PyObject* bullet = PyList_GetItem(bullets_list, i);
        if (!bullet) continue;
        
        // Get rect and velocity
        PyObject* rect = PyObject_GetAttrString(bullet, "rect");
        PyObject* vel = PyObject_GetAttrString(bullet, "vel");
        
        if (!rect || !vel) {
            Py_XDECREF(rect);
            Py_XDECREF(vel);
            continue;
        }
        
        // Get velocity components
        PyObject* vel_x = PyObject_GetAttrString(vel, "x");
        PyObject* vel_y = PyObject_GetAttrString(vel, "y");
        
        if (!vel_x || !vel_y) {
            Py_XDECREF(rect);
            Py_DECREF(vel);
            Py_XDECREF(vel_x);
            Py_XDECREF(vel_y);
            continue;
        }
        
        double vx = PyFloat_AsDouble(vel_x);
        double vy = PyFloat_AsDouble(vel_y);
        
        // Get rect position
        PyObject* rect_x = PyObject_GetAttrString(rect, "x");
        PyObject* rect_y = PyObject_GetAttrString(rect, "y");
        
        if (!rect_x || !rect_y) {
            Py_XDECREF(rect);
            Py_DECREF(vel);
            Py_DECREF(vel_x);
            Py_DECREF(vel_y);
            Py_XDECREF(rect_x);
            Py_XDECREF(rect_y);
            continue;
        }
        
        int x = (int)PyLong_AsLong(rect_x);
        int y = (int)PyLong_AsLong(rect_y);
        
        // Update position
        x += (int)(vx * dt);
        y += (int)(vy * dt);
        
        // Check if offscreen
        PyObject* rect_w = PyObject_GetAttrString(rect, "w");
        PyObject* rect_h = PyObject_GetAttrString(rect, "h");
        
        if (rect_w && rect_h) {
            int w = (int)PyLong_AsLong(rect_w);
            int h = (int)PyLong_AsLong(rect_h);
            
            bool offscreen = (x + w < 0 || x > screen_width ||
                             y + h < 0 || y > screen_height);
            
            if (!offscreen) {
                // Update rect position
                PyObject_SetAttrString(rect, "x", PyLong_FromLong(x));
                PyObject_SetAttrString(rect, "y", PyLong_FromLong(y));
                PyList_Append(result, bullet);
            }
            
            Py_DECREF(rect_w);
            Py_DECREF(rect_h);
        }
        
        Py_DECREF(rect);
        Py_DECREF(vel);
        Py_DECREF(vel_x);
        Py_DECREF(vel_y);
        Py_DECREF(rect_x);
        Py_DECREF(rect_y);
    }
    
    return result;
}

/* Fast distance calculation */
static PyObject* distance_c(PyObject* self, PyObject* args) {
    double x1, y1, x2, y2;
    
    if (!PyArg_ParseTuple(args, "dddd", &x1, &y1, &x2, &y2)) {
        return NULL;
    }
    
    double dx = x2 - x1;
    double dy = y2 - y1;
    double dist = sqrt(dx * dx + dy * dy);
    
    return PyFloat_FromDouble(dist);
}

/* Fast distance squared (avoids sqrt) */
static PyObject* distance_squared_c(PyObject* self, PyObject* args) {
    double x1, y1, x2, y2;
    
    if (!PyArg_ParseTuple(args, "dddd", &x1, &y1, &x2, &y2)) {
        return NULL;
    }
    
    double dx = x2 - x1;
    double dy = y2 - y1;
    double dist_sq = dx * dx + dy * dy;
    
    return PyFloat_FromDouble(dist_sq);
}

/* Batch collision check between bullets and targets */
static PyObject* check_bullet_collisions_c(PyObject* self, PyObject* args) {
    PyObject* bullets_list;
    PyObject* targets_list;
    
    if (!PyArg_ParseTuple(args, "OO", &bullets_list, &targets_list)) {
        return NULL;
    }
    
    Py_ssize_t bullets_len = PyList_Size(bullets_list);
    Py_ssize_t targets_len = PyList_Size(targets_list);
    
    PyObject* collisions = PyList_New(0);
    if (!collisions) return NULL;
    
    for (Py_ssize_t i = 0; i < bullets_len; i++) {
        PyObject* bullet = PyList_GetItem(bullets_list, i);
        if (!bullet) continue;
        
        PyObject* bullet_rect = PyObject_GetAttrString(bullet, "rect");
        if (!bullet_rect) continue;
        
        int bx = (int)PyLong_AsLong(PyObject_GetAttrString(bullet_rect, "x"));
        int by = (int)PyLong_AsLong(PyObject_GetAttrString(bullet_rect, "y"));
        int bw = (int)PyLong_AsLong(PyObject_GetAttrString(bullet_rect, "w"));
        int bh = (int)PyLong_AsLong(PyObject_GetAttrString(bullet_rect, "h"));
        
        Rect bullet_r = {bx, by, bw, bh};
        
        for (Py_ssize_t j = 0; j < targets_len; j++) {
            PyObject* target = PyList_GetItem(targets_list, j);
            if (!target) continue;
            
            PyObject* target_rect = PyObject_GetAttrString(target, "rect");
            if (!target_rect) continue;
            
            int tx = (int)PyLong_AsLong(PyObject_GetAttrString(target_rect, "x"));
            int ty = (int)PyLong_AsLong(PyObject_GetAttrString(target_rect, "y"));
            int tw = (int)PyLong_AsLong(PyObject_GetAttrString(target_rect, "w"));
            int th = (int)PyLong_AsLong(PyObject_GetAttrString(target_rect, "h"));
            
            Rect target_r = {tx, ty, tw, th};
            
            if (rect_collide(&bullet_r, &target_r)) {
                PyObject* collision = Py_BuildValue("(OO)", bullet, target);
                PyList_Append(collisions, collision);
                Py_DECREF(collision);
                break;  // One collision per bullet
            }
            
            Py_DECREF(target_rect);
        }
        
        Py_DECREF(bullet_rect);
    }
    
    return collisions;
}

/* Method definitions */
static PyMethodDef GamePhysicsMethods[] = {
    {"can_move_rect", can_move_rect_c, METH_VARARGS, 
     "Check if a rect can move without collision"},
    {"vec_toward", vec_toward_c, METH_VARARGS,
     "Calculate normalized vector from point A to B"},
    {"update_bullets", update_bullets_c, METH_VARARGS,
     "Batch update bullet positions"},
    {"distance", distance_c, METH_VARARGS,
     "Calculate distance between two points"},
    {"distance_squared", distance_squared_c, METH_VARARGS,
     "Calculate squared distance (faster, no sqrt)"},
    {"check_bullet_collisions", check_bullet_collisions_c, METH_VARARGS,
     "Batch check collisions between bullets and targets"},
    {NULL, NULL, 0, NULL}
};

/* Module definition */
static struct PyModuleDef game_physics_module = {
    PyModuleDef_HEAD_INIT,
    "game_physics",
    "High-performance physics and collision detection",
    -1,
    GamePhysicsMethods
};

/* Module initialization */
PyMODINIT_FUNC PyInit_game_physics(void) {
    return PyModule_Create(&game_physics_module);
}
